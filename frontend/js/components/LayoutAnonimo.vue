<script setup>
import { Link, usePage } from '@inertiajs/vue3';
import IntegracarLogo from './IntegracarLogo.vue';

const page = usePage();
</script>
<template>
    <div class="min-h-dvh flex flex-col">
        <!-- Navbar fixa -->
        <div class="bg-base-300/95 shadow-sm sticky top-0 z-20 border-b border-base-content/10 backdrop-blur">
            <div class="navbar mx-auto w-full max-w-5xl px-3 sm:px-4">
                <div class="flex-1">
                    <Link :href="page.props.urls['index']" class="btn btn-ghost text-base sm:text-xl gap-2 normal-case">
                        <IntegracarLogo />
                        Chatbot IntegraCAR
                    </Link>
                </div>
                <div class="flex gap-2 sm:gap-3">
                    <Link :href="page.props.urls['cadastrar']" class="btn btn-ghost btn-sm sm:btn-md">Cadastrar</Link>
                    <Link :href="page.props.urls['entrar']" class="btn btn-neutral btn-sm sm:btn-md">Entrar</Link>
                </div>
            </div>
        </div>

        <!-- Conteúdo -->
        <div class="grow flex min-h-0 flex-col px-3 pb-3 sm:px-4 sm:pb-4">

            <slot></slot>

        </div>
    </div>
</template>
