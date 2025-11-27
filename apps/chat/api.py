from django.db.models import Q
from django.http import HttpRequest, StreamingHttpResponse
from ninja import Router

from chat.models import Conversa, Mensagem
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

    
    conversa = Conversa.objects.get_or_create(
        id=payload.id_conversa,
        usuario=request.user if request.user.is_authenticated else None,
    )
    if not stream:
        resposta = ''.join(resposta)

        return 200, {'resposta': resposta}

    return StreamingHttpResponse(resposta)
