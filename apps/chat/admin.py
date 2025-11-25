from django.contrib import admin

from chat.models import ChunkDocumeto, Documento


admin.site.register(Documento)
admin.site.register(ChunkDocumeto)