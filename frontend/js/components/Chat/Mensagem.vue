<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { MapMensagens } from './ChatComponente.vue';
import Mensagem from './Mensagem.vue';
import MensagemBot from './MensagemBot.vue';
import MensagemUsuario from './MensagemUsuario.vue';

defineOptions({ name: 'Mensagem' });

const props = defineProps<{
    mapMensagens: MapMensagens;
    ids: number[];
}>();

const indexMensagemSelecionada = ref(props.ids.length - 1);

watch(
    () => props.ids,
    (newIds, oldIds) => {
        if (newIds.length > (oldIds?.length ?? 0)) {
            indexMensagemSelecionada.value = newIds.length - 1;
        } else if (indexMensagemSelecionada.value >= newIds.length) {
            indexMensagemSelecionada.value = newIds.length - 1;
        }
    }
);

const setIndexMensagemSelecionada = (index: number) => {
    if (index < 0 || index >= props.ids.length) return;
    indexMensagemSelecionada.value = index;
};

const mensagemSelecionada = computed(() => {
    const id = props.ids[indexMensagemSelecionada.value];
    return props.mapMensagens[id] ?? null;
});

const mensagemFilhaRef = ref<typeof Mensagem | null>(null);

function obterIdUltimaMensagem(): number {
    if (mensagemSelecionada.value.mensagens_filhas.length === 0) return mensagemSelecionada.value.id;
    return mensagemFilhaRef.value?.obterIdUltimaMensagem() || mensagemSelecionada.value.id;
}

defineExpose({
    obterIdUltimaMensagem,
});

</script>

<template>
    <div v-if="!mensagemSelecionada" class="text-red-500 text-sm">
        Mensagem não encontrada.
    </div>

    <template v-else>
        <MensagemBot v-if="mensagemSelecionada.tipo === 'ASSISTENTE'" :mensagem="mensagemSelecionada"
            :index-mensagem-selecionada="indexMensagemSelecionada" :max-mensagem-selecionada="ids.length - 1"
            :setIndexMensagemSelecionada="setIndexMensagemSelecionada" />

        <MensagemUsuario v-else-if="mensagemSelecionada.tipo === 'USUARIO'" :mensagem="mensagemSelecionada"
            :index-mensagem-selecionada="indexMensagemSelecionada" :max-mensagem-selecionada="ids.length - 1"
            :setIndexMensagemSelecionada="setIndexMensagemSelecionada" />

        <!-- Recursão -->
        <Mensagem ref="mensagemFilhaRef" v-if="mensagemSelecionada.mensagens_filhas.length"
            :map-mensagens="mapMensagens" :ids="mensagemSelecionada.mensagens_filhas" />
    </template>
</template>
