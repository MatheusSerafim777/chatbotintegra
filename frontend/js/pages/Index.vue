<script setup>
import ChatAnonimo from '@/pages/Chat/ChatAnonimo.vue'
import Chat from '@/pages/Chat/Chat.vue'
import { ref } from 'vue'
import { usePage } from '@inertiajs/vue3'
const page = usePage()
</script>

<template>
    <Chat v-if="page.props.user" />
    <ChatAnonimo v-else />
</template>
