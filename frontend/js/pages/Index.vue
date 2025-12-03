<script setup lang="ts">
import ChatAnonimo from '@/pages/Chat/ChatAnonimo.vue'
import Chat from '@/pages/Chat/Chat.vue'
import { usePage } from '@inertiajs/vue3'
import { Usuario } from '@/types/index';

const page = usePage < { user: Usuario | null } > ()
</script>

<template>
    <Chat v-if="page.props.user" />
    <ChatAnonimo v-else />
</template>
