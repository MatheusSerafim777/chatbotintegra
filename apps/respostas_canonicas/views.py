import json
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from inertia import render

from chat.models import RespostaCanonica
from respostas_canonicas.forms import RespostaCanonicaForm

# Create your views here.


@method_decorator(login_required, name='dispatch')
class CuradoriaView(View):
    def get(self, request: HttpRequest):
        respostas_canonicas = RespostaCanonica.objects.all()
        context = {
            'respostas_canonicas': respostas_canonicas,
        }
        return render(request, 'Curadoria/Curadoria', context)


@method_decorator(login_required, name='dispatch')
class CadastrarCanonicaView(View):
    form_class = RespostaCanonicaForm

    def get(self, request: HttpRequest):
        context = {'form': self.form_class()}
        return render(request, 'Curadoria/CadastrarCanonica', context)
    
    def post(self, request: HttpRequest):
        form = self.form_class(json.loads(request.body))
        if not form.is_valid():
            context = {'form': form}
            return render(request, 'Curadoria/CadastrarCanonica', context)
        form.save()
        return redirect('curadoria')

    
class ExcluirCanonicaView(View):
    def post(self, request:HttpRequest, id_canonica:int):
        canonica = get_object_or_404(RespostaCanonica, id=id_canonica)
        canonica.delete()
        return redirect('curadoria')    
        
