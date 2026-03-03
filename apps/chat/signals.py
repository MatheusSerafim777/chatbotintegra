import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_q.tasks import Chain

from chat.models import Documento, StatusDocumento
from chat.rag import Rag

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Documento)
def set_nome_documento(sender: type[Documento], instance: Documento, **kwargs):
    if not instance.nome:
        instance.nome = instance.arquivo.name


@receiver(post_save, sender=Documento)
def create_embedding_documento(
    sender: type[Documento],
    instance: Documento,
    created: bool,
    **kwargs,
):
    # Só enfileira tasks se o documento estiver PENDENTE.
    # Isso evita loop infinito: as tasks usam update() para não
    # re-disparar este signal, mas caso usem save(), a checagem
    # de status impede a re-criação de chains.
    if instance.status != StatusDocumento.PENDENTE:
        return

    logger.info(f'Enfileirando processamento do documento {instance.id}')
    chain = Chain()
    chain.append(Rag.extrair_e_salvar_conteudo, id_documento=instance.id)
    chain.append(Rag.gerar_e_embedar_chunks, id_documento=instance.id)
    chain.run()
