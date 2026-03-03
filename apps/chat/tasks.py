import logging

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter

from chat.models import ChunkDocumeto, Documento, StatusDocumento
from chat.rag import Rag

logger = logging.getLogger(__name__)


def gerar_embedding_documento(documento_id: int):
    """Task legada - mantida por compatibilidade.
    Prefira usar a chain via signal (extrair_e_salvar_conteudo + gerar_e_embedar_chunks).
    """
    # Usa update() para não disparar o signal post_save
    updated = Documento.objects.filter(
        id=documento_id,
        status=StatusDocumento.PENDENTE,
    ).update(status=StatusDocumento.PROCESSANDO)

    if not updated:
        logger.warning(
            f'Documento {documento_id} não está PENDENTE. '
            f'Abortando (possível execução duplicada).'
        )
        return

    try:
        documento = Documento.objects.get(id=documento_id)

        text_splitter = TokenTextSplitter(
            chunk_size=512,
            chunk_overlap=256,
        )

        conteudo = PyPDFLoader(documento.arquivo.path, mode='single').load()

        chunks = text_splitter.split_documents(conteudo)
        chunks = [chunk.page_content.replace('\n', '') for chunk in chunks]

        if not chunks:
            logger.error(f'Documento {documento_id}: nenhum chunk gerado.')
            Documento.objects.filter(id=documento_id).update(
                status=StatusDocumento.ERRO,
            )
            return

        embeddings = Rag.embedding.embed_documents(chunks)

        embeddings = [
            ChunkDocumeto(
                documento=documento,
                conteudo=chunk,
                embedding=embedding,
            )
            for chunk, embedding in zip(chunks, embeddings, strict=False)
        ]

        documento.embeddings.all().delete()

        ChunkDocumeto.objects.bulk_create(embeddings)

        # Usa update() para não disparar o signal post_save
        Documento.objects.filter(id=documento_id).update(
            status=StatusDocumento.PROCESSADO,
        )
        logger.info(f'Documento {documento_id}: processado com sucesso.')
    except Exception as e:
        logger.exception(f'Erro ao processar documento {documento_id}: {e}')
        Documento.objects.filter(id=documento_id).update(
            status=StatusDocumento.ERRO,
        )
        raise
