import json

from django.db import transaction
from django.http import HttpRequest, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from chat.models import Conversa, Documento, Mensagem
from chat.rag import Rag
from chat.schemas import ChatSchema, CurtirMensagemSchema

chat_router = Router()


@chat_router.post('/chat')
def chat_endpoint(request: HttpRequest, payload: ChatSchema):
    mensagem = payload.mensagem
    stream = payload.stream

    if not mensagem:
        return 400, {'resposta': 'Mensagem vazia'}

    # Criar objetos no banco de forma atômica
    with transaction.atomic():
        if payload.id_conversa:
            conversa = Conversa.objects.select_for_update().get(
                id=payload.id_conversa,
                usuario=request.user,
            )
        else:
            conversa = Conversa.objects.create(usuario=request.user)

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

    resposta = Rag.run(mensagem)

    if not stream:
        resposta_completa = ''.join(resposta)
        Mensagem.objects.filter(id=mensagem_resposta.id).update(
            conteudo=resposta_completa
        )
        return 200, base_response | {'resposta': resposta_completa}

    def resposta_streaming():
        yield json.dumps(base_response) + '\n'
        chunks = []
        for chunk_resposta in resposta:
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
def status_documento(request, id_documento):
    documento = get_object_or_404(Documento, id=id_documento)
    return {'status': documento.status}


@chat_router.patch('/mensagens/{id_mensagem}/curtir')
def curtir_mensagem(
    request: HttpRequest,
    id_mensagem: int,
    payload: CurtirMensagemSchema,
):
    mensagem = get_object_or_404(
        Mensagem, id=id_mensagem, conversa__usuario=request.user
    )
    mensagem.curtido = payload.curtido
    mensagem.save(update_fields=['curtido'])
    return {'curtido': mensagem.curtido}
