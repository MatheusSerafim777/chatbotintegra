from __future__ import annotations

from contas.models import Usuario
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Field
from django.db.models.lookups import PostgresOperatorLookup
from pgvector.django import VectorField

from chat.indexes import BM25Index


@Field.register_lookup
class BM25(PostgresOperatorLookup):
    lookup_name = 'bm25'
    postgres_operator = '@@@'


class StatusDocumento(models.TextChoices):
    PENDENTE = 'pendente', 'Pendente'
    PROCESSANDO = 'processando', 'Processando'
    PROCESSADO = 'processado', 'Processado'


class Documento(models.Model):
    nome = models.CharField(max_length=255, blank=True)
    arquivo = models.FileField(
        upload_to='documentos/',
        validators=[FileExtensionValidator(['pdf'])],
    )
    conteudo = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusDocumento.choices,
        default=StatusDocumento.PENDENTE,
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    embeddings: models.QuerySet[ChunkDocumeto]

    def __str__(self):
        return self.nome


class ChunkDocumeto(models.Model):
    documento = models.ForeignKey(
        Documento,
        on_delete=models.CASCADE,
        related_name='embeddings',
    )
    conteudo = models.TextField()
    embedding = VectorField(dimensions=1536)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            BM25Index(
                fields=['id', 'conteudo'],
                key_field='id',
                name='bm25_index_conteudo',
            ),
        ]

    def __str__(self):
        return self.conteudo[:50]


class RespostaCanonica(models.Model):
    pergunta = models.TextField()
    embedding = VectorField()
    resposta = models.TextField()

    def __str__(self):
        return self.pergunta


class Conversa(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='conversas',
    )
    nome = models.CharField(max_length=50)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Mensagem(models.Model):
    class OpcoesTipo(models.TextChoices):
        USUARIO = 'USUARIO', 'Usuário'
        ASSISTENTE = 'ASSISTENTE', 'Assistente'

    conversa = models.ForeignKey(
        Conversa,
        on_delete=models.CASCADE,
        related_name='mensagens',
    )

    mensagem_anterior = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='filhos',
        null=True,
        blank=True,
    )

    resposta_canonica = models.ForeignKey(
        RespostaCanonica,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    tipo_usuario = models.CharField(
        max_length=20,
        choices=OpcoesTipo.choices,
    )

    like = models.BooleanField(
        null=True,
        blank=True,
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    conteudo = models.TextField()

    def __str__(self):
        return self.conteudo[:50]
