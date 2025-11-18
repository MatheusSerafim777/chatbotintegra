import sys

from django.contrib.messages import get_messages
from django.http import HttpRequest
from inertia import share


class DataShareMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

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

        response = self.get_response(request)

        return response


class FlushStdoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        sys.stdout.flush()
        return response
