from django.contrib import admin

from chat.models import ChunkDocumeto, Conversa, Documento, Mensagem

admin.site.register(Documento)
admin.site.register(ChunkDocumeto)
admin.site.register(Conversa)
admin.site.register(Mensagem)
