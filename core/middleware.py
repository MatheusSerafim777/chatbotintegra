import sys

from chat.models import Conversa
from django.contrib.messages import get_messages
from django.db.models import Max
from django.http import HttpRequest
from django.urls import get_resolver
from inertia import share


class DataShareMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def get_urls(self) -> dict[str, str]:
        urls = {}
        resolver = get_resolver()
        for name, route in resolver.reverse_dict.items():
            if not isinstance(name, str):
                continue
            pattern = route[0][0]

            url = pattern[0]

            urls[name] = '/' + url
        return urls

    def __call__(self, request: HttpRequest):
        messages = []
        for message in get_messages(request):
            messages.append({
                'message': message.message,
                'level': message.level,
                'tags': message.tags,
                'extra_tags': message.extra_tags,
                'level_tag': message.level_tag,
            })

        share(request, messages=messages)

        share(
            request,
            user=lambda: request.user
            if request.user.is_authenticated
            else None,
        )

        share(
            request,
            urls=self.get_urls,
        )

        conversas = []
        if request.user.is_authenticated:
            conversas = (
                Conversa.objects.filter(usuario=request.user)
                .annotate(ultima_mensagem_at=Max('mensagens__criado_em'))
                .order_by('-ultima_mensagem_at')
            )

        share(
            request,
            conversas=conversas,
        )

        response = self.get_response(request)

        return response


class FlushStdoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        sys.stdout.flush()
        return response
