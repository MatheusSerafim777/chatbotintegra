<script setup lang="ts">
import { TMensagem } from './ChatComponente.vue';
import { ref } from 'vue';

const props = defineProps<{
    mensagem: TMensagem,
    indexMensagemSelecionada: number;
    maxMensagemSelecionada: number;
    setIndexMensagemSelecionada: (index: number) => void;
}>();

const copiado = ref(false);

function escapeHtml(str: string): string {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;")
        .replace(/\n/g, '<br>');
}

async function copiarMensagem() {
    try {
        await navigator.clipboard.writeText(props.mensagem.conteudo);
        copiado.value = true;
        setTimeout(() => {
            copiado.value = false;
        }, 2000);
    } catch (error) {
        console.error('Erro ao copiar mensagem:', error);
    }
}

</script>

<template>
    <div class="flex flex-col items-end gap-2 group">
        <div
            class="max-w-lg px-4 py-1.5 rounded-[18px] bg-neutral text-neutral-content whitespace-pre-wrap wrap-break-word">
            <p v-html="escapeHtml(mensagem.conteudo)"></p>
        </div>
        <div
            class="flex gap-0 opacity-0 pointer-events-none transition hover:transition-none group-hover:opacity-100 group-hover:pointer-events-auto">
            <button class="btn btn-ghost btn-xs btn-square" @click="copiarMensagem">
                <i class="text-base" :class="copiado ? 'bi bi-check-lg' : 'bi bi-copy'"></i>
            </button>
            <button class="btn btn-ghost btn-xs btn-square">
                <i class="bi bi-pencil text-base"></i>
            </button>
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
        </div>
    </div>
</template>