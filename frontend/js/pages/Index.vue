<script setup>
import ChatAnonimo from '@/pages/Chat/ChatAnonimo.vue'
import Chat from '@/pages/Chat/Chat.vue'
import { ref } from 'vue'
import { usePage } from '@inertiajs/vue3'
const page = usePage()

const mensagens = ref([
    { tipo: 'usuario', mensagem: 'Olá, como posso ajudar?' },
    { tipo: 'bot', mensagem: 'Olá! Em que posso ajudar você hoje?' },
    { tipo: 'usuario', mensagem: 'Quais são os seus horários de atendimento?' },
    { tipo: 'bot', mensagem: 'Nosso horário de atendimento é de segunda a sexta, das 9h às 18h.' },
]);

</script>

<template>
    <Chat v-if="page.props.user" :mensagens="mensagens" />
    <ChatAnonimo />
</template>
