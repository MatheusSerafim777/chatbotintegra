<script setup lang="ts">
import { Mensagem } from './ChatComponente.vue';
import markdownit from 'markdown-it';


const md = markdownit();


defineProps<{
    mensagem: Mensagem,
    indexMensagemSelecionada: number;
    maxMensagemSelecionada: number;
    setIndexMensagemSelecionada: (index: number) => void;
}>();

</script>

<template>
    <div class="flex flex-col items-start gap-2 mt-4 group text-black">

        <div v-if="mensagem.conteudo" class="markdown" v-html="md.render(mensagem.conteudo)"></div>
        <div v-else class="inline-grid *:[grid-area:1/1]">
            <div class="status status-neutral animate-ping status-lg"></div>
            <div class="status status-neutral status-lg"></div>
        </div>

        <div class="flex gap-0">
            <div class="flex items-center gap-0.5" v-if="maxMensagemSelecionada > 0">
                <button class="btn btn-ghost btn-xs btn-square" :disabled="indexMensagemSelecionada <= 0"
                    @click="setIndexMensagemSelecionada(indexMensagemSelecionada - 1)">
                    <i class="bi bi-caret-left text-base"></i>
                </button>
                <span class="text-sm h-fit">{{ indexMensagemSelecionada + 1 }}/{{ maxMensagemSelecionada + 1 }}</span>
                <button class="btn btn-ghost btn-xs btn-square"
                    @click="setIndexMensagemSelecionada(indexMensagemSelecionada + 1)"
                    :disabled="indexMensagemSelecionada >= maxMensagemSelecionada">
                    <i class="bi bi-caret-right text-base"></i>
                </button>
            </div>
            <button class="btn btn-ghost btn-xs btn-square">
                <i class="bi bi-copy text-base"></i>
            </button>
            <button class="btn btn-ghost btn-xs btn-square">
                <i class="bi bi-hand-thumbs-up text-base"></i>
            </button>
            <button class="btn btn-ghost btn-xs btn-square">
                <i class="bi bi-hand-thumbs-down text-base"></i>
            </button>
            <button class="btn btn-ghost btn-xs btn-square">
                <i class="bi bi-arrow-repeat text-base"></i>
            </button>
        </div>
    </div>
</template>