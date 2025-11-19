import json

from django.contrib.auth import login, logout
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views import View
from inertia import InertiaResponse, render

from contas.forms import CadastroForm, SigninForm


class LoginView(View):
    template_name = 'Contas/Login'
    form_class = SigninForm

    def get(self, request: HttpRequest) -> InertiaResponse:
        context = {
            'form': self.form_class(),
        }
        return render(
            request,
            self.template_name,
            context,
        )

    def post(self, request: HttpRequest) -> InertiaResponse:
        dados = json.loads(request.body)

        form = self.form_class(request, dados)

        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, self.template_name, context)

        login(request, form.get_user())

        if isinstance(dados, dict) and not dados.get('remember'):
            request.session.set_expiry(0)

        return redirect('index')


class CadastroView(View):
    form_class = CadastroForm
    template = 'Contas/Cadastro'

    def get(self, request: HttpRequest):
        context = {
            'form': self.form_class(),
        }
        return render(request, self.template, context)

    def post(self, request: HttpRequest) -> InertiaResponse:
        dados = json.loads(request.body)

        form = self.form_class(dados)
        if not form.is_valid():
            context = {'form': form}
            return render(request, self.template, context)

        form.save()

        login(request, form.instance)

        if isinstance(dados, dict) and not dados.get('remember'):
            request.session.set_expiry(0)

        return redirect('index')


class SairView(View):
    def post(self, request: HttpRequest):
        logout(request)
        return redirect('index')
