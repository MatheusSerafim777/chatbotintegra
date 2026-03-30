import logging
import re
from collections import defaultdict
from typing import Generator, Literal, TypedDict
import unicodedata

import httpx
from django.conf import settings
from django.db.models import (
    F,
    QuerySet,
    Value,
    Window,
)
from django.db.models.functions import Rank
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pgvector.django import CosineDistance

from chat.functions import BM25Score, PdbQueryCast
from chat.models import ChunkDocumeto, Documento, Mensagem, StatusDocumento

logger = logging.getLogger(__name__)


class ClassificacaoResponse(TypedDict):
    classe: Literal['Manual', 'Legislação']
    confianca: float




def normalize(text: str) -> str:
    STOPWORDS = {"a", "o", "e", "de", "da", "do", "para", "em"}
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS]

    return " ".join(tokens)

class Rag:
    chat = ChatOpenAI(
        model='gpt-4.1-mini-2025-04-14',
        temperature=0.5,
        api_key=settings.OPENAI_API_KEY,
    )

    embedding = OpenAIEmbeddings(
        model='text-embedding-3-small',
        dimensions=1536,
        api_key=settings.OPENAI_API_KEY,
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    MAPA_CLASSE_API_PARA_MODEL = {
        'Manual': Documento.Tipo.MANUAL,
        'Legislação': Documento.Tipo.LEGISLACAO,
    }

    @staticmethod
    def extrair_e_salvar_conteudo(id_documento: int) -> None:

        # Usa update() para mudar status sem disparar post_save signal
        updated = Documento.objects.filter(
            id=id_documento,
            status=StatusDocumento.PENDENTE,
        ).update(status=StatusDocumento.PROCESSANDO)

        if not updated:
            logger.warning(
                f'Documento {id_documento} não está PENDENTE '
                f'(possível execução duplicada). Abortando extração.'
            )
            return

        try:
            documento = Documento.objects.get(id=id_documento)

            conteudo = ' '.join([
                d.page_content
                for d in PyPDFLoader(
                    documento.arquivo.path, mode='single'
                ).load()
            ])

            conteudo = re.sub(r'\s+', ' ', conteudo).strip()

            if not conteudo:
                logger.error(
                    f'Documento {id_documento}: conteúdo extraído está vazio.'
                )
                Documento.objects.filter(id=id_documento).update(
                    status=StatusDocumento.ERRO,
                )
                return

            # Usa update() para não disparar o signal post_save
            Documento.objects.filter(id=id_documento).update(
                conteudo=conteudo,
                status=StatusDocumento.PROCESSANDO,
            )
            logger.info(
                f'Documento {id_documento}: conteúdo extraído '
                f'({len(conteudo)} caracteres).'
            )
        except Exception as e:
            logger.exception(
                f'Erro ao extrair conteúdo do documento {id_documento}: {e}'
            )
            Documento.objects.filter(id=id_documento).update(
                status=StatusDocumento.ERRO,
            )
            raise

    # Tamanho máximo de batch para chamadas de embedding (evita timeout)
    EMBEDDING_BATCH_SIZE = 100

    @staticmethod
    def gerar_e_embedar_chunks(id_documento: int) -> None:
        documento = Documento.objects.get(id=id_documento)

        # Verifica se o documento está em estado válido para processamento
        if documento.status not in {
            StatusDocumento.PROCESSANDO,
        }:
            logger.warning(
                f'Documento {id_documento} não está PROCESSANDO '
                f'(status={documento.status}). Abortando geração de chunks.'
            )
            return

        if not documento.conteudo:
            logger.error(
                f'Documento {id_documento} não possui conteúdo. '
                f'Abortando geração de chunks.'
            )
            Documento.objects.filter(id=id_documento).update(
                status=StatusDocumento.ERRO,
            )
            return

        try:
            documento.embeddings.all().delete()

            chunks = Rag.splitter.split_text(documento.conteudo)

            if not chunks:
                logger.error(
                    f'Documento {id_documento}: splitter retornou 0 chunks.'
                )
                Documento.objects.filter(id=id_documento).update(
                    status=StatusDocumento.ERRO,
                )
                return

            logger.info(
                f'Documento {id_documento}: gerando embeddings '
                f'para {len(chunks)} chunks.'
            )

            # Processa embeddings em batches para evitar timeout
            # em documentos grandes
            all_embeddings = []
            for i in range(0, len(chunks), Rag.EMBEDDING_BATCH_SIZE):
                batch = chunks[i : i + Rag.EMBEDDING_BATCH_SIZE]
                batch_embeddings = Rag.embedding.embed_documents(batch)
                all_embeddings.extend(batch_embeddings)

            chunks_documento = [
                ChunkDocumeto(
                    documento=documento,
                    conteudo=chunk,
                    embedding=embedding,
                )
                for chunk, embedding in zip(
                    chunks, all_embeddings, strict=False
                )
            ]

            ChunkDocumeto.objects.bulk_create(chunks_documento)

            # Usa update() para não disparar o signal post_save
            Documento.objects.filter(id=id_documento).update(
                status=StatusDocumento.PROCESSADO,
            )
            logger.info(
                f'Documento {id_documento}: processado com sucesso '
                f'({len(chunks)} chunks criados).'
            )
        except Exception as e:
            logger.exception(
                f'Erro ao gerar chunks do documento {id_documento}: {e}'
            )
            Documento.objects.filter(id=id_documento).update(
                status=StatusDocumento.ERRO,
            )
            raise

    @staticmethod
    def top_k_bm25(query: str, k: int) -> QuerySet[ChunkDocumeto]:
        qs = (
            ChunkDocumeto.objects.filter(
                conteudo__bm25=PdbQueryCast(
                    Value('{"match": {"value": "%s"}}' % query)
                ),
            )
            .annotate(score=BM25Score('id'))
            .order_by('-score')[:k]
        )

        return qs

    @staticmethod
    def top_k_similar(query: str, k: int) -> QuerySet[ChunkDocumeto]:
        embedding_query = Rag.embedding.embed_query(query)

        qs = ChunkDocumeto.objects.annotate(
            score=CosineDistance(
                'embedding',
                embedding_query,
            ),
        ).order_by('score')[:k]

        return qs

    @staticmethod
    def top_k_chunks(query: str, k: int = 5) -> list[str]:  # noqa
        embedding_query = Rag.embedding.embed_query(query)

        ranked_by_bm25 = (
            ChunkDocumeto.objects.annotate(
                score=BM25Score('id'),
                rank=Window(expression=Rank(), order_by=F('score').desc()),
            )
            .filter(
                conteudo__bm25=PdbQueryCast(
                    Value(
                        f'{{"match": {{"value": "{normalize(query)}"}}}}'
                    )
                )
            )
            .order_by('-score')
        )

        ranked_by_semantic = ChunkDocumeto.objects.annotate(
            score=CosineDistance('embedding', embedding_query),
            rank=Window(expression=Rank(), order_by=F('score').asc()),
        ).order_by('score')

        response: ClassificacaoResponse = httpx.post(
            'http://redeneuralbert:8000/classificar',
            json={'texto': query},
        ).json()

        tipo_documento = Rag.MAPA_CLASSE_API_PARA_MODEL.get(response['classe'])
        CONFIANCA_MINIMA = 0.6 + 1
        if response['confianca'] >= CONFIANCA_MINIMA and tipo_documento:
            ranked_by_bm25 = ranked_by_bm25.filter(
                documento__tipo=tipo_documento
            )
            ranked_by_semantic = ranked_by_semantic.filter(
                documento__tipo=tipo_documento
            )

        ranked_by_bm25 = ranked_by_bm25[: k * 4]
        ranked_by_semantic = ranked_by_semantic[: k * 4]

        agrupado = defaultdict(list)
        for chunk in ranked_by_bm25:
            agrupado[chunk.id].append(('bm25', chunk))
        for chunk in ranked_by_semantic:
            agrupado[chunk.id].append(('semantic', chunk))

        bm25_weight = 0.5
        semantic_weight = 0.5
        combinado = []

        RRF_CONSTANT = 60 

        for chunks in agrupado.values():
            rank_bm25 = next((c.rank for t, c in chunks if t == 'bm25'), None)
            rank_sem = next((c.rank for t, c in chunks if t == 'semantic'), None)

            # Se não foi encontrado em um dos métodos, o score daquele método é 0
            score_bm25 = 1.0 / (RRF_CONSTANT + rank_bm25) if rank_bm25 else 0.0
            score_sem = 1.0 / (RRF_CONSTANT + rank_sem) if rank_sem else 0.0

            # Você pode manter seus pesos se quiser dar mais força para a semântica ou exata
            total_score = (bm25_weight * score_bm25) + (semantic_weight * score_sem)

            representante = chunks[0][1]
            representante.score = total_score
            combinado.append(representante)

        combinado.sort(key=lambda x: x.score, reverse=True)
        qs = combinado[:k]
        return [chunk.conteudo for chunk in qs]

    @staticmethod
    def run(
        query: str,
        mensagens: QuerySet[Mensagem],
    ) -> Generator[str, None, None]:
        contexto = '\n\n\n'.join(Rag.top_k_chunks(query, k=10))

        # 1. System Prompt Consolidado e com Persona Forte
        system_prompt = """Você é um assistente corporativo especialista em análise documental.
Sua missão é responder às perguntas dos usuários de forma precisa, clara e amigável.

REGRAS DE COMPORTAMENTO:
- Você pode responder cumprimentos e se apresentar, mas sempre redirecione a conversa para o assunto principal: responder às perguntas sobre CAR.
- Responda SEMPRE em português.
- Use formatação Markdown (negrito, listas, blocos de código) para facilitar a leitura.
- Adicione emojis moderadamente para manter o tom conversacional e agradável.
- Você é estritamente limitado aos documentos fornecidos. Nunca use conhecimentos prévios externos.
- Se a resposta não estiver clara ou não existir no contexto fornecido, você DEVE responder exatamente: "Não tenho informações sobre isso."
- Não invente, não faça suposições e não tente adivinhar respostas."""

        mensagens_formatadas = [
            SystemMessage(system_prompt),
            *[
                HumanMessage(m.conteudo)
                if m.tipo == Mensagem.OpcoesTipo.USUARIO
                else AIMessage(m.conteudo)
                for m in mensagens
            ],
        ]

        # 2. Injeção do Contexto com Tags XML (Ajuda a IA a separar as coisas)
        # O contexto entra no final, colado com a pergunta, para evitar o "viés de recência"
        prompt_final_usuario = f"""Aqui está o documento de referência para a sua resposta:

<contexto>
{contexto}
</contexto>

{query}"""

        mensagens_formatadas.append(HumanMessage(prompt_final_usuario))

        for resposta in Rag.chat.stream(mensagens_formatadas):
            yield resposta
