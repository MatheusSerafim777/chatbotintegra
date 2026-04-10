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
    <article class="mt-1 flex flex-col items-end gap-2" aria-label="Mensagem do usuário">
        <div
            class="max-w-[92%] sm:max-w-2xl rounded-2xl bg-neutral px-4 py-2.5 text-neutral-content whitespace-pre-wrap wrap-break-word shadow-sm">
            <p v-html="escapeHtml(mensagem.conteudo)"></p>
        </div>
        <div class="flex flex-wrap items-center gap-1 px-1 py-1">
            <button class="btn btn-ghost btn-xs btn-square" @click="copiarMensagem" aria-label="Copiar mensagem"
                :title="copiado ? 'Copiado' : 'Copiar mensagem'">
                <i class="text-base" :class="copiado ? 'bi bi-check-lg' : 'bi bi-copy'"></i>
            </button>
            <div class="flex items-center gap-0.5" v-if="maxMensagemSelecionada > 0" aria-label="Navegação entre versões">
                <button class="btn btn-ghost btn-xs btn-square" :disabled="indexMensagemSelecionada <= 0"
                    aria-label="Versão anterior" title="Versão anterior"
                    @click="setIndexMensagemSelecionada(indexMensagemSelecionada - 1)">
                    <i class="bi bi-caret-left text-base"></i>
                </button>
                <span class="text-xs h-fit px-1">{{ indexMensagemSelecionada + 1 }}/{{ maxMensagemSelecionada + 1 }}</span>
                <button class="btn btn-ghost btn-xs btn-square"
                    aria-label="Próxima versão" title="Próxima versão"
                    @click="setIndexMensagemSelecionada(indexMensagemSelecionada + 1)"
                    :disabled="indexMensagemSelecionada >= maxMensagemSelecionada">
                    <i class="bi bi-caret-right text-base"></i>
                </button>
            </div>
        </div>
    </article>
</template>
