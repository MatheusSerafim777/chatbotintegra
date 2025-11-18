import json

from django.contrib.auth import login
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views import View
from inertia import InertiaResponse, render

from contas.forms import SigninForm


class LoginView(View):
    form_class = SigninForm

    def get(self, request: HttpRequest) -> InertiaResponse:
        context = {
            'form': self.form_class(),
        }
        return render(
            request,
            'Contas/Login',
            context,
        )

    def post(self, request: HttpRequest) -> InertiaResponse:
        form = self.form_class(request, json.loads(request.body))

        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'Contas/Login', context)

        login(request, form.get_user())

        return redirect('index')
