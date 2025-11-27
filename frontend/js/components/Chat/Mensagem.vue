<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { MapMensagens } from './ChatComponente.vue';
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
    (newIds) => {
        indexMensagemSelecionada.value = newIds.length - 1;
    }
);

const mensagemSelecionada = computed(() => {
    const id = props.ids[indexMensagemSelecionada.value];
    return props.mapMensagens[id] ?? null;
});

const setIndexMensagemSelecionada = (index: number) => {
    if (index < 0 || index >= props.ids.length) return;
    indexMensagemSelecionada.value = index;
};
</script>

<template>
    <div v-if="!mensagemSelecionada" class="text-red-500 text-sm">
        Mensagem não encontrada.
    </div>

    <template v-else>
        <MensagemBot v-if="mensagemSelecionada.tipo === 'bot'" :mensagem="mensagemSelecionada"
            :index-mensagem-selecionada="indexMensagemSelecionada" :max-mensagem-selecionada="ids.length - 1"
            :setIndexMensagemSelecionada="setIndexMensagemSelecionada" />

        <MensagemUsuario v-else-if="mensagemSelecionada.tipo === 'usuario'" :mensagem="mensagemSelecionada"
            :index-mensagem-selecionada="indexMensagemSelecionada" :max-mensagem-selecionada="ids.length - 1"
            :setIndexMensagemSelecionada="setIndexMensagemSelecionada" />

        <!-- Recursão -->
        <Mensagem v-if="mensagemSelecionada.mensagensFilhas.length" :map-mensagens="mapMensagens"
            :ids="mensagemSelecionada.mensagensFilhas" />
    </template>
</template>
