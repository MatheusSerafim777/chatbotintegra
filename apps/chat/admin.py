from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from chat.models import ChunkDocumeto, Conversa, Documento, Mensagem


class MensagemResource(resources.ModelResource):
    class Meta:
        model = Mensagem
        fields = (
            'id',
            'conversa',
            'mensagem_pai',
            'resposta_canonica',
            'conteudo',
            'tipo',
            'curtido',
            'criado_em',
            'created_at',
            'updated_at',
        )
        export_order = fields

admin.site.register(Documento)
@admin.register(Mensagem)
class MensagemAdmin(ImportExportModelAdmin):
    resource_class = MensagemResource
    list_display = (
        'id',
        'conversa',
        'tipo',
        'resumo_conteudo',
        'mensagem_pai',
        'resposta_canonica',
        'curtido',
        'criado_em',
    )
    ordering = ('-criado_em',)
    list_filter = ('tipo', 'curtido', 'criado_em')
    search_fields = ['conteudo', 'conversa__nome', 'resposta_canonica__pergunta']
    raw_id_fields = ('conversa', 'mensagem_pai', 'resposta_canonica')

    @admin.display(description='Conteúdo')
    def resumo_conteudo(self, mensagem: Mensagem):
        if len(mensagem.conteudo) <= 80:
            return mensagem.conteudo
        return f'{mensagem.conteudo[:77]}...'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'conversa',
            'mensagem_pai',
            'resposta_canonica',
        )


@admin.register(ChunkDocumeto)
class ChunkDocumentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'documento')
    ordering = ('id',)
    search_fields = ['conteudo']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('documento')


@admin.register(Conversa)
class ConversaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'criado_em', 'ver_conversa')
    ordering = ('-criado_em',)

    @admin.display(description='Ver')
    def ver_conversa(self, conversa: Conversa):
        return mark_safe(  # noqa
            f'<a target="_blank" href="{reverse("conversa", args=[conversa.pk])}">Ver</a>'
        )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usuario')
