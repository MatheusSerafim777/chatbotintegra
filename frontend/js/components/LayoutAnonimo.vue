<script setup>
import { Link, usePage } from '@inertiajs/vue3';
import IntegracarLogo from './IntegracarLogo.vue';

const page = usePage();
</script>
<template>
    <div class="min-h-dvh flex flex-col">
        <!-- Navbar fixa -->
        <div class="bg-linear-to-r/shorter from-neutral to-base-300 shadow-sm sticky top-0 z-20 border-b border-base-content/10 backdrop-blur">
            <div class="navbar mx-auto w-full max-w-5xl px-3 sm:px-4">
                <div class="flex-1">
                    <Link :href="page.props.urls['index']" class="flex items-center gap-2 p-0 text-white">
                        <IntegracarLogo />
                        Chatbot IntegraCAR
                    </Link>
                </div>
                <div class="flex gap-2 sm:gap-3">
                    <Link :href="page.props.urls['cadastrar']" class="btn btn-ghost btn-sm sm:btn-md text-white">Cadastrar</Link>
                    <Link :href="page.props.urls['entrar']" class="btn btn-neutral btn-sm sm:btn-md">Entrar</Link>
                </div>
            </div>
        </div>

        <!-- Conteúdo -->
        <div class="grow flex min-h-0 flex-col overflow-y-auto overflow-x-hidden px-3 pb-3 sm:px-4 sm:pb-4">

            <slot></slot>

        </div>
    </div>
</template>
