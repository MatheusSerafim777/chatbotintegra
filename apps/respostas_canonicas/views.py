import json

from chat.models import RespostaCanonica
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from inertia import render

from respostas_canonicas.forms import RespostaCanonicaForm
from django.urls import reverse
# Create your views here.

@method_decorator(login_required, name='dispatch')
class RespostasCanonicasView(View):
    def get(self, request: HttpRequest):
        respostas_canonicas = RespostaCanonica.objects.all().order_by('id')
        context = {
            'respostas_canonicas': respostas_canonicas,
        }
        return render(request, 'Curadoria/Curadoria', context)


@method_decorator(login_required, name='dispatch')
class CadastrarCanonicaView(View):
    template_name = 'Curadoria/RespostaCanonicaForm'
    form_class = RespostaCanonicaForm

    def get_context_data(self, form: RespostaCanonicaForm):
        return {
            'form': form,
            'action_url': reverse('cadastro_canonica'),
            'titulo': 'Cadastrar Canônica',
            'button_text': 'Salvar',
        }

    def get(self, request: HttpRequest):
        context = {'form': self.form_class(), 'titulo':"Cadastrar Canônica"}
        return render(request, 'Curadoria/CadastrarCanonica', context)
    
    def post(self, request: HttpRequest):
        form = self.form_class(json.loads(request.body))

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                self.get_context_data(self.form_class()),
            )

        form.save()
        return redirect('curadoria')


class ExcluirCanonicaView(View):
    def post(self, request: HttpRequest, id_canonica: int):
        canonica = get_object_or_404(RespostaCanonica, id=id_canonica)
        canonica.delete()
        return redirect('curadoria')


class EditarCanonicaView(View):
    template_name = 'Curadoria/RespostaCanonicaForm'
    form_class = RespostaCanonicaForm

    def get_context_data(self, form: RespostaCanonicaForm):
        return {
            'form': form,
            'action_url': reverse('editar_canonica', args=[form.instance.id]),
            'titulo': 'Editar Canônica',
            'button_text': 'Salvar Alterações',
        }

    def get(self, request, id_canonica):
        canonica = get_object_or_404(RespostaCanonica, id=id_canonica)
        form = RespostaCanonicaForm(instance=canonica)

        return render(request, 'Curadoria/EditarCanonica', {
            "form": form,
            "urls": {
                "curadoria": reverse("curadoria"),
                "editar": reverse("editar_canonica", args=[id_canonica]),
            },
        })
 
    def post(self, request: HttpRequest, id_canonica):
        canonica = get_object_or_404(RespostaCanonica, id=id_canonica)
        form = RespostaCanonicaForm(json.loads(request.body), instance=canonica)

        if not form.is_valid():
            return render(request, 'Curadoria/EditarCanonica', {
                "form": form,
                "urls": {
                    "curadoria": reverse("curadoria"),
                    "editar": reverse("editar_canonica", args=[id_canonica]),
                }
            })

        form.save()
        return redirect('curadoria')
