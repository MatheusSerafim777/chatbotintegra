from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views import View
from inertia import render

# Create your views here.


@method_decorator(login_required, name='dispatch')
class CuradoriaView(View):
    def get(self, request: HttpRequest):
        return render(request, 'Curadoria/Curadoria')


@method_decorator(login_required, name='dispatch')
class CadastrarCanonicaView(View):
    def get(self, request: HttpRequest):
        return render(request, 'Curadoria/CadastrarCanonica')
