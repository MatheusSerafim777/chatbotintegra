from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from inertia import render

from chat.forms import ImportarDocumentosForm
from chat.models import Documento, StatusDocumento


@method_decorator(csrf_exempt, name='dispatch')
class IndexView(View):
    def get(self, request: HttpRequest):
        return render(request, 'Index')


@method_decorator(login_required, name='dispatch')
class DocumentosView(View):
    template_name = 'Chat/Documentos'
    form_class = ImportarDocumentosForm

    def get(self, request: HttpRequest, extra_context=None):
        documentos = Documento.objects.all()

        documentos_processados = documentos.filter(
            status=StatusDocumento.PROCESSADO
        ).count()

        documentos_pendentes = documentos.filter(
            status__in=[
                StatusDocumento.PENDENTE,
                StatusDocumento.PROCESSANDO,
            ]
        ).count()

        context = {
            'importar_documentos_form': ImportarDocumentosForm(),
            'documentos': documentos,
            'documentos_processados': documentos_processados,
            'documentos_pendentes': documentos_pendentes,
        } | (extra_context or {})
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest):
        form = self.form_class({}, request.FILES)
        if not form.is_valid():
            return self.get(request, {'importar_documentos_form': form})

        form.save()

        return redirect('documentos')
    
class ExcluirDocumentoView(View):
    def post(self, request:HttpRequest, id:int):
        documento = get_object_or_404(Documento, id=id)
        documento.delete()
        return redirect('documentos')
