from django.http import StreamingHttpResponse
from ninja import Router

from chat.rag import Rag
from chat.schemas import ChatSchema

chat_router = Router()


@chat_router.post('/chat')
def chat_endpoint(request, payload: ChatSchema):
    mensagem = payload.mensagem
    stream = payload.stream

    if not mensagem:
        return 400, {'resposta': 'Mensagem vazia'}

    resposta = Rag.run(mensagem)

    if not stream:
        resposta = ''.join(resposta)
        return 200, {'resposta': resposta}

    return StreamingHttpResponse(resposta)
