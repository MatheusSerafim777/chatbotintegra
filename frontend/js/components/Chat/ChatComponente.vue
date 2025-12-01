<script setup lang="ts">
import { ref, nextTick, computed } from 'vue';
import Mensagem from './Mensagem.vue';

export type TMensagem = {
    id: number;
    tipo: 'usuario' | 'bot',
    conteudo: string;
    mensagemPai: number | null;
    mensagensFilhas: number[];
    curtido: boolean | null;
}

export type MapMensagens = {
    [key: number]: TMensagem;
}

const mapMensagens = ref<MapMensagens>({
    // 1: { id: 1, tipo: 'bot', conteudo: 'Olá! Como posso ajudar você hoje?', mensagemPai: null, mensagensFilhas: [2, 3], curtido: null },
    // 2: { id: 2, tipo: 'usuario', conteudo: 'Oi! Oque é CAR?', mensagemPai: 1, mensagensFilhas: [], curtido: null },
    // 3: { id: 3, tipo: 'usuario', conteudo: 'Preciso de ajuda com meu processo.', mensagemPai: 1, mensagensFilhas: [6, 7], curtido: null },
    // 4: { id: 4, tipo: 'bot', conteudo: 'Olá! Precisa de ajuda?', mensagemPai: null, mensagensFilhas: [5], curtido: null },
    // 5: { id: 5, tipo: 'usuario', conteudo: 'Sim, por favor.', mensagemPai: 4, mensagensFilhas: [], curtido: null },
    // 6: { id: 6, tipo: 'bot', conteudo: 'Claro! Com o que você precisa de ajuda?', mensagemPai: 3, mensagensFilhas: [], curtido: null },
    // 7: { id: 7, tipo: 'bot', conteudo: 'Estou aqui para ajudar com seu processo.', mensagemPai: 3, mensagensFilhas: [], curtido: null },
});

const mensagensRaiz = computed<number[]>(() => Object.values(mapMensagens.value).filter(mensagem => mensagem.mensagemPai === null).map(mensagem => mensagem.id!));

const pergunta = ref('');
const editable = ref<HTMLElement | null>(null);
const containerMensagens = ref<HTMLElement | null>(null);
const mensagemRef = ref<typeof Mensagem | null>(null);

async function adicionarMensagem(mensagem: TMensagem) {
    mapMensagens.value[mensagem.id] = mensagem;
    await nextTick();
    scrollParaUltimaMensagem();
}

const enviarMensagem = async () => {
    if (!pergunta.value.trim()) return;

    const mensagemPaiSelecionada = mensagensRaiz.value.length > 0 ? mensagemRef.value?.obterIdUltimaMensagem() : null;
    console.log('Mensagem pai selecionada:', mensagemPaiSelecionada);
    const mensagemUsuario: TMensagem = {
        id: Date.now() + Math.random(),
        tipo: 'usuario',
        conteudo: pergunta.value,
        mensagemPai: mensagemPaiSelecionada,
        mensagensFilhas: [],
        curtido: null,
    };
    if (mensagemPaiSelecionada !== null) {
        mapMensagens.value[mensagemPaiSelecionada].mensagensFilhas.push(mensagemUsuario.id);
    }
    await adicionarMensagem(mensagemUsuario);


    const lastUserMessage = pergunta.value;
    pergunta.value = '';
    if (editable.value) {
        editable.value.textContent = '';
    }

    // mensagem vazia do bot
    const botMessage: TMensagem = {
        id: Date.now() + Math.random(),
        tipo: 'bot',
        conteudo: '',
        mensagemPai: mensagemUsuario.id,
        mensagensFilhas: [],
        curtido: null,
    };
    mapMensagens.value[mensagemUsuario.id].mensagensFilhas.push(botMessage.id);
    await adicionarMensagem(botMessage);

    // Agora começa o streaming
    const response = await fetch('/api/chat', {
        method: 'POST',
        body: JSON.stringify({
            mensagem: lastUserMessage,
            stream: true
        }),
    });

    if (!response.body) {
        return;
    }
    // faça uma tabela simples, sem `
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        mapMensagens.value[botMessage.id].conteudo += decoder.decode(value); //input de escrita
        scrollParaUltimaMensagem();
    };
}


function handlePaste(e: ClipboardEvent) {
    e.preventDefault()
    const text = e.clipboardData?.getData('text/plain') || ''
    document.execCommand('insertText', false, text)
}

function scrollParaUltimaMensagem() {
    const div = containerMensagens.value
    if (div) {
        div.scrollTo({
            top: div.scrollHeight,
            behavior: 'smooth',
        })
    }
}

</script>

<template>
    <div class="flex-1 pb-4 mx-auto flex flex-col justify-between w-full">
        <div class="overflow-auto flex-1 max-h-[85vh]" ref="containerMensagens">
            <div class="w-full max-w-3xl mx-auto py-2">
                <Mensagem ref="mensagemRef" v-if="mensagensRaiz.length > 0" :map-mensagens="mapMensagens"
                    :ids="mensagensRaiz" />
            </div>
        </div>
        <form @submit.prevent="enviarMensagem" class="w-full max-w-3xl mx-auto">
            <label for="pergunta"
                class="relative flex justify-between items-center gap-4 min-h-14 rounded-[28px] bg-base-300 text-base-content shadow-2xl shadow-base-300 p-2.5 cursor-text"
                @click="editable?.focus()">

                <!-- placeholder -->
                <span v-if="!pergunta.trim()"
                    class="absolute left-2.5 top-1/2 -translate-y-1/2 text-base-content/50 pointer-events-none select-none">
                    Digite sua mensagem...
                </span>
                <div class="w-full max-h-60 overflow-scroll">
                    <div ref="editable" id="pergunta" contenteditable="true" role="textbox" aria-multiline="true"
                        class="w-full bg-transparent focus:outline-none p-0 font-medium min-h-6 whitespace-pre-wrap wrap-break-word"
                        @input="pergunta = editable?.innerText ?? ''"
                        @keydown="if ($event.key === 'Enter') { if (!$event.shiftKey) { $event.preventDefault(); enviarMensagem(); } }"
                        @paste="handlePaste">
                    </div>
                </div>

                <button class="btn btn-neutral text-neutral-content h-9 w-9 btn-circle p-0"
                    :disabled="!pergunta.trim()">
                    <i class="bi bi-arrow-up-short text-4xl h-9 w-9"></i>
                </button>
            </label>
        </form>

    </div>
</template>