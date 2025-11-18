from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
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
    template_name = 'ia/documentos.html'

    def get(self, request: HttpRequest):
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
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class ImportarDocumentosView(View):
    form_class = ImportarDocumentosForm

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST, request.FILES)
        if not form.is_valid():
            context = {'form': form}
            return render(request, 'components/form.html', context)

        form.save()

        # return HttpResponseClientRefresh()
