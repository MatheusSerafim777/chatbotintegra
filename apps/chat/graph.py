from __future__ import annotations

import logging
import re
from typing import Literal, TypedDict

from django.db.models import QuerySet
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from chat.models import Documento, Mensagem
from chat.rag import Rag

logger = logging.getLogger(__name__)


class AnalisePergunta(BaseModel):
    """Saída estruturada do agente que entende e direciona a pergunta."""

    pergunta_reescrita: str = Field(min_length=1)
    dominio: Literal[
        'manual',
        'legislacao',
        'ambos',
        'nao_documental',
        'precisa_esclarecimento',
    ]
    subperguntas: list[str] = Field(default_factory=list)


class ChatState(TypedDict, total=False):
    pergunta: str
    historico: list[dict[str, str]]
    analise: dict
    resposta: str


ANALISADOR_PROMPT = """Você é o agente analisador de um chatbot corporativo.
Analise a pergunta atual considerando o histórico fornecido.

Regras:
- Reescreva perguntas curtas ou dependentes do histórico para que sejam
  autossuficientes.
- Use 'manual' para procedimentos e uso do sistema.
- Use 'legislacao' para leis, normas, artigos, obrigações e prazos legais.
- Use 'ambos' quando a pergunta exigir norma e procedimento operacional.
- Use 'nao_documental' para cumprimentos e conversa casual.
- Perguntas definicionais claras, como 'O que é CAR?', são autossuficientes;
  não peça esclarecimento nesses casos.
- Use 'precisa_esclarecimento' quando faltar informação essencial.
- Não responda à pergunta; retorne apenas a análise estruturada.
"""


def _pergunta_definicional_autossuficiente(pergunta: str) -> bool:
    """Evita pedir esclarecimento para perguntas curtas, mas completas."""
    pergunta_normalizada = pergunta.strip().casefold().replace('é', 'e')
    correspondencia = re.fullmatch(
        r'(?:o que e|o que significa|para que serve) (.+?)[?!.]*',
        pergunta_normalizada,
    )
    if not correspondencia:
        return False

    assunto = correspondencia.group(1).strip()
    return assunto not in {'isso', 'isto', 'aquilo', 'ele', 'ela'}


RESPOSTA_APROFUNDADA_PROMPT = """Produza uma resposta aprofundada, mas objetiva.
Não responda apenas com uma frase quando a pergunta exigir explicação.

Siga esta estrutura sempre que fizer sentido:
1. Conclusão direta.
2. Explicação do contexto e do motivo.
3. Passo a passo ou aplicação prática.
4. Condições, exceções e pontos de atenção.
5. Fontes ou trechos utilizados, somente quando identificáveis no contexto.

Responda a todas as subperguntas explicitamente. Use listas e subtítulos em
Markdown. Não aumente o texto com informações que não estejam nas fontes.
"""


def _historico_mensagens(historico: list[dict[str, str]]):
    mensagens = []
    for mensagem in historico:
        conteudo = mensagem.get('content')
        if not conteudo:
            continue
        if mensagem.get('role') == 'user':
            mensagens.append(HumanMessage(conteudo))
        else:
            mensagens.append(AIMessage(conteudo))
    return mensagens


def _analisar_pergunta(state: ChatState) -> ChatState:
    prompt = (
        f"Histórico da conversa:\n{state.get('historico', [])}\n\n"
        f"Pergunta atual:\n{state['pergunta']}"
    )

    try:
        analisador = Rag.chat.with_structured_output(AnalisePergunta)
        analise = analisador.invoke(
            [SystemMessage(ANALISADOR_PROMPT), HumanMessage(prompt)]
        )
    except Exception:
        logger.exception('Falha no agente analisador; usando rota Ambos.')
        analise = AnalisePergunta(
            pergunta_reescrita=state['pergunta'],
            dominio='ambos',
        )

    # Uma pergunta definicional com assunto explícito não precisa de uma
    # rodada adicional de esclarecimento. Mantemos a busca nos dois domínios
    # para aumentar a chance de encontrar a definição nos documentos.
    if (
        analise.dominio == 'precisa_esclarecimento'
        and _pergunta_definicional_autossuficiente(state['pergunta'])
    ):
        analise = analise.model_copy(update={'dominio': 'ambos'})

    return {'analise': analise.model_dump()}


def _rota(state: ChatState) -> str:
    return state['analise']['dominio']


def _resposta_nao_documental(state: ChatState) -> ChatState:
    return {
        'resposta': (
            'Olá! Posso ajudar com dúvidas sobre os procedimentos do sistema '
            'e a legislação relacionada ao CAR. Como posso ajudar?'
        )
    }


def _pedir_esclarecimento(state: ChatState) -> ChatState:
    return {
        'resposta': (
            'Pode fornecer mais detalhes sobre o procedimento, documento ou '
            'norma que deseja consultar?'
        )
    }


def _responder_com_especialista(
    state: ChatState,
    tipo_documento: Documento.Tipo,
    nome_especialista: str,
    instrucoes: str,
) -> str:
    pergunta = state['analise']['pergunta_reescrita']
    subperguntas = state['analise'].get('subperguntas', [])
    consulta = '\n'.join([pergunta, *subperguntas])
    contexto = '\n\n\n'.join(
        Rag.top_k_chunks(
            consulta,
            k=12,
            tipo_documento=tipo_documento,
        )
    )

    system_prompt = f"""Você é o {nome_especialista} do chatbot IntegraCAR.
Responda sempre em português e use somente o contexto fornecido.
Se o contexto não contiver a resposta, diga que não há informação suficiente.
Não invente dados nem use conhecimento externo.

{RESPOSTA_APROFUNDADA_PROMPT}

{instrucoes}
"""
    mensagens = [
        SystemMessage(system_prompt),
        *_historico_mensagens(state.get('historico', [])),
        HumanMessage(
            f'<contexto>\n{contexto}\n</contexto>\n\n'
            f'Pergunta:\n{pergunta}\n\n'
            f'Subperguntas a cobrir:\n{subperguntas}'
        ),
    ]
    resposta = Rag.chat.invoke(mensagens)
    return str(resposta.content)


def _responder_manual(state: ChatState) -> ChatState:
    resposta = _responder_com_especialista(
        state,
        Documento.Tipo.MANUAL,
        'especialista em manuais operacionais',
        (
            'Priorize pré-requisitos, passos em ordem, campos, telas, '
            'mensagens de erro e resultado esperado.'
        ),
    )
    return {'resposta': resposta}


def _responder_legislacao(state: ChatState) -> ChatState:
    resposta = _responder_com_especialista(
        state,
        Documento.Tipo.LEGISLACAO,
        'especialista em análise documental da legislação',
        (
            'Diferencie obrigação, permissão, proibição e exceção. Cite a '
            'norma e o artigo quando essas informações estiverem no contexto.'
        ),
    )
    return {'resposta': resposta}


def _responder_ambos(state: ChatState) -> ChatState:
    resposta_manual = _responder_com_especialista(
        state,
        Documento.Tipo.MANUAL,
        'especialista em manuais operacionais',
        'Priorize passos, pré-requisitos e resultado esperado.',
    )
    resposta_legislacao = _responder_com_especialista(
        state,
        Documento.Tipo.LEGISLACAO,
        'especialista em análise documental da legislação',
        'Cite normas e artigos quando estiverem no contexto.',
    )

    sintese = Rag.chat.invoke(
        [
            SystemMessage(
                'Você sintetiza respostas de Manual e Legislação. '
                'Responda em português, mantenha as fontes separadas e '
                'aponte divergências sem inventar informações.\n\n'
                f'{RESPOSTA_APROFUNDADA_PROMPT}'
            ),
            HumanMessage(
                f"Pergunta: {state['analise']['pergunta_reescrita']}\n\n"
                f"Resposta do Manual:\n{resposta_manual}\n\n"
                f"Resposta da Legislação:\n{resposta_legislacao}"
            ),
        ]
    )
    return {'resposta': str(sintese.content)}


def build_chat_graph():
    builder = StateGraph(ChatState)
    builder.add_node('analisar_pergunta', _analisar_pergunta)
    builder.add_node('resposta_nao_documental', _resposta_nao_documental)
    builder.add_node('pedir_esclarecimento', _pedir_esclarecimento)
    builder.add_node('especialista_manual', _responder_manual)
    builder.add_node('especialista_legislacao', _responder_legislacao)
    builder.add_node('especialistas_ambos', _responder_ambos)

    builder.add_edge(START, 'analisar_pergunta')
    builder.add_conditional_edges(
        'analisar_pergunta',
        _rota,
        {
            'nao_documental': 'resposta_nao_documental',
            'precisa_esclarecimento': 'pedir_esclarecimento',
            'manual': 'especialista_manual',
            'legislacao': 'especialista_legislacao',
            'ambos': 'especialistas_ambos',
        },
    )

    for node in (
        'resposta_nao_documental',
        'pedir_esclarecimento',
        'especialista_manual',
        'especialista_legislacao',
        'especialistas_ambos',
    ):
        builder.add_edge(node, END)

    return builder.compile()


CHAT_GRAPH = build_chat_graph()


def run_chat_graph(query: str, mensagens: QuerySet[Mensagem]):
    historico = [
        {
            'role': (
                'user'
                if mensagem.tipo == Mensagem.OpcoesTipo.USUARIO
                else 'assistant'
            ),
            'content': mensagem.conteudo,
        }
        for mensagem in mensagens
    ]
    resultado = CHAT_GRAPH.invoke(
        {
            'pergunta': query,
            'historico': historico,
        }
    )
    yield resultado['resposta']
