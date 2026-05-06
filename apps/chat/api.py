import json

from django.db import transaction
from django.http import HttpRequest, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django_cte import CTE, with_cte
from ninja import Router
from openai import APIConnectionError

from chat.models import Conversa, Documento, Mensagem
from chat.rag import Rag
from chat.schemas import (
    AtualizarTipoDocumentoSchema,
    ChatSchema,
    CurtirMensagemSchema,
)

chat_router = Router()


@chat_router.post('/chat')
def chat_endpoint(request: HttpRequest, payload: ChatSchema):
    mensagem = payload.mensagem
    stream = payload.stream

    if not mensagem:
        return 400, {'resposta': 'Mensagem vazia'}

    def mensagens_cte(cte: CTE):
        values = ('id', 'mensagem_pai_id', 'conteudo', 'criado_em')
        return (
            Mensagem.objects.filter(
                conversa_id=payload.id_conversa,
                id=payload.id_mensagem_pai,
            )
            .values(*values)
            .union(
                cte.join(Mensagem, id=cte.col.mensagem_pai_id).values(*values),
                all=True,
            )
        )

    cte = CTE.recursive(mensagens_cte)
    mensagens = with_cte(
        cte, select=cte.join(Mensagem, id=cte.col.id).order_by('criado_em')
    )

    # Criar objetos no banco de forma atômica
    with transaction.atomic():
        if payload.id_conversa:
            conversa = Conversa.objects.select_for_update().get(
                id=payload.id_conversa,
                usuario=request.user
                if request.user.is_authenticated
                else None,
            )
        else:
            tamanho_maximo = 20
            conversa = Conversa.objects.create(
                usuario=request.user
                if request.user.is_authenticated
                else None,
                nome=mensagem[:tamanho_maximo] + '...'
                if len(mensagem) > tamanho_maximo
                else mensagem,
            )

        mensagem_pai = None
        if payload.id_mensagem_pai:
            mensagem_pai = (
                Mensagem.objects.filter(
                    id=payload.id_mensagem_pai,
                    conversa_id=conversa.id,
                )
                .only('id')
                .first()
            )

        mensagem_pergunta = Mensagem.objects.create(
            conversa_id=conversa.id,
            conteudo=mensagem,
            mensagem_pai=mensagem_pai,
            tipo=Mensagem.OpcoesTipo.USUARIO,
        )

        mensagem_resposta = Mensagem.objects.create(
            conversa_id=conversa.id,
            mensagem_pai_id=mensagem_pergunta.id,
            tipo=Mensagem.OpcoesTipo.ASSISTENTE,
            conteudo='',
        )

    base_response = {
        'id_conversa': conversa.id,
        'id_mensagem_pergunta': mensagem_pergunta.id,
        'id_mensagem_resposta': mensagem_resposta.id,
    }

    resposta = Rag.run(mensagem, mensagens)

    if not stream:
        resposta_completa = ''.join(resposta)
        Mensagem.objects.filter(id=mensagem_resposta.id).update(
            conteudo=resposta_completa
        )
        return 200, base_response | {'resposta': resposta_completa}

    def resposta_streaming():
        yield json.dumps(base_response) + '\n'
        chunks = []
        try:
            for chunk_resposta in resposta:
                chunks.append(chunk_resposta)
                yield chunk_resposta
        except APIConnectionError:
            chunk_resposta = (
                '\n\nUm erro inesperado ocorreu durante a gereção da resposta.'
            )
            chunks.append(chunk_resposta)
            yield chunk_resposta

        Mensagem.objects.filter(id=mensagem_resposta.id).update(
            conteudo=''.join(chunks)
        )

    return StreamingHttpResponse(
        resposta_streaming(),
        content_type='text/plain; charset=utf-8',
    )


@chat_router.get('/documentos/{id_documento}/status')
def status_documento(request: HttpRequest, id_documento: int):
    documento = get_object_or_404(Documento, id=id_documento)
    return {'status': documento.status}


@chat_router.patch('/documentos/{id_documento}/tipo')
def atualizar_tipo_documento(
    request: HttpRequest,
    id_documento: int,
    payload: AtualizarTipoDocumentoSchema,
):
    documento = get_object_or_404(Documento, id=id_documento)
    tipo = payload.tipo

    documento.tipo = tipo
    documento.save(update_fields=['tipo'])

    return 400, {'error': 'Tipo inválido'}


@chat_router.patch('/mensagens/{id_mensagem}/curtir')
def curtir_mensagem(
    request: HttpRequest,
    id_mensagem: int,
    payload: CurtirMensagemSchema,
):
    mensagem = get_object_or_404(Mensagem, id=id_mensagem)
    mensagem.curtido = payload.curtido
    mensagem.save(update_fields=['curtido'])
    return {'curtido': mensagem.curtido}
