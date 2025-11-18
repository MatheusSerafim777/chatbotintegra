<script setup lang="ts">
import { Link } from '@inertiajs/vue3';
import Mensagem from '@/components/Chat/Mensagem.vue';


import { ref } from "vue"
import LayoutAnonimo from '@/components/LayoutAnonimo.vue';
import Layout from '@/components/Layout.vue';


const mensagens = ref([
    { tipo: 'usuario', mensagem: 'Olá, como posso ajudar?' },
    { tipo: 'bot', mensagem: 'Olá! Em que posso ajudar você hoje?' },
    { tipo: 'usuario', mensagem: 'Quais são os seus horários de atendimento?' },
    { tipo: 'bot', mensagem: 'Nosso horário de atendimento é de segunda a sexta, das 9h às 18h.' },
]);


const pergunta = ref('');

const enviarMensagem = async () => {
    if (!pergunta.value.trim()) return;

    mensagens.value.push({
        tipo: 'usuario',
        mensagem: pergunta.value
    });

    const lastUserMessage = pergunta.value;
    pergunta.value = '';

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
    <Layout>
        <div class="max-w-3xl h-full max-h-[calc(100vh-6rem)] mx-auto flex flex-col gap-6">
            <div class="grow max-h-full overflow-x-auto overflow-y-visible p-2">
                <Mensagem v-for="(m, i) in mensagens" :key="i" :mensagem="m.mensagem" :tipo="m.tipo" />
            </div>
            <form @submit.prevent="enviarMensagem">
                <label for="pergunta"
                    class="flex justify-between items-center gap-4 min-h-14 rounded-[28px] bg-base-200 border border-base-300 shadow p-3 cursor-text">
                    <input id="pergunta"
                        class="input input-ghost w-full bg-transparent focus:outline-none h-fit p-0 font-medium"
                        placeholder="Digite sua mensagem..." v-model="pergunta" autofocus />

                    <button class="btn btn-xs btn-circle p-0" :disabled="!pergunta.trim()">
                        <i class="bi bi-arrow-up-circle-fill text-4xl"></i>
                    </button>
                </label>
            </form>
        </div>
    </Layout>
</template>
