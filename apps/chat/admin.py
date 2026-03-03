from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from chat.models import ChunkDocumeto, Conversa, Documento, Mensagem

admin.site.register(Documento)
admin.site.register(ChunkDocumeto)
admin.site.register(Mensagem)


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
