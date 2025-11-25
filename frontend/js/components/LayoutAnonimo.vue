<script setup>
import { Link, usePage } from '@inertiajs/vue3';

const page = usePage();
</script>
<template>
    <div class="min-h-screen flex flex-col">
        <!-- Navbar fixa -->
        <div class="bg-base-200 shadow-sm sticky top-0 z-20">
            <div class="navbar mx-auto max-w-3xl">
                <div class="flex-1">
                    <Link :href="page.props.urls['sair']" class="btn btn-ghost text-xl">
                    Chabot IntegraCAR
                    </Link>
                </div>
                <div class="flex gap-4">
                    <Link :href="page.props.urls['cadastrar']" class="btn btn-ghost">Cadastrar</Link>
                    <Link :href="page.props.urls['entrar']" class="btn btn-neutral">Entrar</Link>
                </div>
            </div>
        </div>

        <!-- Conteúdo -->
        <div class="grow">

            <slot></slot>

        </div>
    </div>
</template>
