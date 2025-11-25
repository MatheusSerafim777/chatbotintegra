<script setup lang="ts">
import { ref } from 'vue';
import Mensagem from './Mensagem.vue';

const mensagens = ref([
    { tipo: 'usuario', mensagem: 'Olá, como posso ajudar?' },
    { tipo: 'bot', mensagem: 'Olá! Em que posso ajudar você hoje?' },
    { tipo: 'usuario', mensagem: 'Quais são os seus horários de atendimento?' },
    { tipo: 'bot', mensagem: 'Nosso horário de atendimento é de segunda a sexta, das 9h às 18h.' },
    { tipo: 'usuario', mensagem: 'Olá, como posso ajudar?' },
    { tipo: 'bot', mensagem: 'Olá! Em que posso ajudar você hoje?' },
    { tipo: 'usuario', mensagem: 'Quais são os seus horários de atendimento?' },
    { tipo: 'bot', mensagem: 'Nosso horário de atendimento é de segunda a sexta, das 9h às 18h.' },
    { tipo: 'usuario', mensagem: 'Olá, como posso ajudar?' },
    { tipo: 'bot', mensagem: 'Olá! Em que posso ajudar você hoje?' },
    { tipo: 'usuario', mensagem: 'Quais são os seus horários de atendimento?' },
    { tipo: 'bot', mensagem: 'Nosso horário de atendimento é de segunda a sexta, das 9h às 18h.' },
]);


const pergunta = ref('');
const editable = ref<HTMLElement | null>(null);

const enviarMensagem = async () => {
    if (!pergunta.value.trim()) return;

    mensagens.value.push({
        tipo: 'usuario',
        mensagem: pergunta.value
    });

    const lastUserMessage = pergunta.value;
    pergunta.value = '';
    if (editable.value) {
        editable.value.innerText = '';
    }

    // mensagem vazia do bot
    const botMessage = { tipo: 'bot', mensagem: '' };
    mensagens.value.push(botMessage);

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

    const index = mensagens.value.length - 1;
    while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        mensagens.value[index].mensagem += decoder.decode(value);
    }
};

</script>

<template>
    <div class="h-full pb-4 mx-auto flex flex-col justify-between gap-6">
        <div class="overflow-auto max-h-[81vh]">
            <div class="w-full max-w-3xl mx-auto py-2">
                <Mensagem v-for="(m, i) in mensagens" :key="i" :mensagem="m.mensagem" :tipo="m.tipo" />
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
                        @keydown="if ($event.key === 'Enter') { if (!$event.shiftKey) { $event.preventDefault(); enviarMensagem(); } }">
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