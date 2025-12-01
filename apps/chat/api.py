from django.http import HttpRequest, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from chat.models import Documento
from chat.rag import Rag
from chat.schemas import ChatSchema

chat_router = Router()


@chat_router.post('/chat')
def chat_endpoint(request: HttpRequest, payload: ChatSchema):
    mensagem = payload.mensagem
    stream = payload.stream

    if not mensagem:
        return 400, {'resposta': 'Mensagem vazia'}

    resposta = Rag.run(mensagem)

    if not stream:
        resposta = ''.join(resposta)

        return 200, {'resposta': resposta}

    return StreamingHttpResponse(resposta)


@chat_router.get('/documentos/{id_documento}/status')
def status_documento(request, id_documento):
    documento = get_object_or_404(Documento, id=id_documento)
    return {'status': documento.status}
