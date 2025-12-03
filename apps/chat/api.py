import json

from django.db import transaction
from django.http import HttpRequest, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from chat.models import Conversa, Documento, Mensagem
from chat.rag import Rag
from chat.schemas import ChatSchema

chat_router = Router()


@chat_router.post('/chat')
@transaction.atomic
def chat_endpoint(request: HttpRequest, payload: ChatSchema):
    mensagem = payload.mensagem
    stream = payload.stream

    if not mensagem:
        return 400, {'resposta': 'Mensagem vazia'}

    conversa, _ = Conversa.objects.get_or_create(
        id=payload.id_conversa,
        usuario=request.user,
    )

    mensagem_pai = None
    if payload.id_mensagem_pai:
        mensagem_pai = Mensagem.objects.filter(
            id=payload.id_mensagem_pai,
            conversa=conversa,
        ).first()

    mensagem_pergunta = Mensagem.objects.create(
        conversa=conversa,
        conteudo=mensagem,
        mensagem_pai=mensagem_pai,
        tipo=Mensagem.OpcoesTipo.USUARIO,
    )

    mensagem_resposta = Mensagem.objects.create(
        conversa=conversa,
        mensagem_pai=mensagem_pergunta,
        tipo=Mensagem.OpcoesTipo.ASSISTENTE,
    )

    base_response = {
        'id_conversa': conversa.id,
        'id_mensagem_pergunta': mensagem_pergunta.id,
        'id_mensagem_resposta': mensagem_resposta.id,
    }

    resposta = Rag.run(mensagem)

    if not stream:
        resposta = ''.join(resposta)
        mensagem_resposta.conteudo = resposta
        mensagem_resposta.save()
        return 200, base_response | {'resposta': resposta}

    def resposta_streaming():
        yield json.dumps(base_response) + '\n'
        for chunk_resposta in resposta:
            mensagem_resposta.conteudo += chunk_resposta
            yield chunk_resposta
        mensagem_resposta.save()

    return StreamingHttpResponse(resposta_streaming())


@chat_router.get('/documentos/{id_documento}/status')
def status_documento(request, id_documento):
    documento = get_object_or_404(Documento, id=id_documento)
    return {'status': documento.status}
