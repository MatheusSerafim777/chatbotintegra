<script setup lang="ts">
import MensagemBot from './MensagemBot.vue';
import MensagemUsuario from './MensagemUsuario.vue';

defineProps < {
    mensagem: string,
    tipo: string,
} > ();
</script>

<template>
    <MensagemUsuario v-if="tipo === 'usuario'" :mensagem="mensagem" />
    <MensagemBot v-else :mensagem="mensagem" />
</template>