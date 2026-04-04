<script setup lang="ts">
import { TMensagem } from './ChatComponente.vue';
import markdownit from 'markdown-it';
import { ref, watch } from 'vue';


const md = markdownit();


const props = defineProps<{
    mensagem: TMensagem,
    indexMensagemSelecionada: number;
    maxMensagemSelecionada: number;
    setIndexMensagemSelecionada: (index: number) => void;
}>();

const curtido = ref<boolean | null>(props.mensagem.curtido);
const copiado = ref(false);

watch(() => props.mensagem.curtido, (novoCurtido) => {
    curtido.value = novoCurtido;
});

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

async function curtirMensagem(valor: boolean) {
    const novoValor = curtido.value === valor ? null : valor;

    try {
        const response = await fetch(`/api/mensagens/${props.mensagem.id}/curtir`, {
            method: 'PATCH',
            body: JSON.stringify({ curtido: novoValor }),
        });

        if (response.ok) {
            curtido.value = novoValor;
            props.mensagem.curtido = novoValor;
        }
    } catch (error) {
        console.error('Erro ao curtir mensagem:', error);
    }
}
</script>

<template>
    <article class="mt-4 flex flex-col items-start gap-2" aria-label="Mensagem do assistente">

        <div v-if="mensagem.conteudo"
            class="markdown w-full rounded-2xl bg-base-100"
            v-html="md.render(mensagem.conteudo)"></div>
        <div v-else class="inline-grid *:[grid-area:1/1] pl-1" aria-label="Assistente digitando resposta">
            <div class="status status-neutral animate-ping status-lg"></div>
            <div class="status status-neutral status-lg"></div>
        </div>

        <div class="flex flex-wrap items-center gap-1">
            <div class="flex items-center gap-0.5" v-if="maxMensagemSelecionada > 0" aria-label="Navegação entre respostas">
                <button class="btn btn-ghost btn-xs btn-square" :disabled="indexMensagemSelecionada <= 0"
                    aria-label="Resposta anterior" title="Resposta anterior"
                    @click="setIndexMensagemSelecionada(indexMensagemSelecionada - 1)">
                    <i class="bi bi-caret-left text-base"></i>
                </button>
                <span class="text-xs h-fit px-1">{{ indexMensagemSelecionada + 1 }}/{{ maxMensagemSelecionada + 1 }}</span>
                <button class="btn btn-ghost btn-xs btn-square"
                    aria-label="Próxima resposta" title="Próxima resposta"
                    @click="setIndexMensagemSelecionada(indexMensagemSelecionada + 1)"
                    :disabled="indexMensagemSelecionada >= maxMensagemSelecionada">
                    <i class="bi bi-caret-right text-base"></i>
                </button>
            </div>
            <button class="btn btn-ghost btn-xs btn-square" @click="copiarMensagem" aria-label="Copiar mensagem"
                :title="copiado ? 'Copiado' : 'Copiar mensagem'">
                <i class="text-base" :class="copiado ? 'bi bi-check-lg' : 'bi bi-copy'"></i>
            </button>
            <button v-if="curtido !== false" class="btn btn-ghost btn-xs btn-square" @click="curtirMensagem(true)"
                aria-label="Curtir resposta" title="Curtir resposta"
                :class="{ 'text-success': curtido === true }">
                <i class="text-base"
                    :class="curtido === true ? 'bi bi-hand-thumbs-up-fill' : 'bi bi-hand-thumbs-up'"></i>
            </button>
            <button v-if="curtido !== true" class="btn btn-ghost btn-xs btn-square" @click="curtirMensagem(false)"
                aria-label="Não curtir resposta" title="Não curtir resposta"
                :class="{ 'text-error': curtido === false }">
                <i class="text-base"
                    :class="curtido === false ? 'bi bi-hand-thumbs-down-fill' : 'bi bi-hand-thumbs-down'"></i>
            </button>
        </div>
    </article>
</template>
