<script setup lang="ts">
import { Link } from '@inertiajs/vue3';
</script>
<template>
    <div class="min-h-screen flex flex-col">
        <!-- Navbar fixa -->
        <div class="bg-base-200 shadow-sm sticky top-0 z-20">
            <div class="navbar mx-auto max-w-3xl">
                <div class="flex-1">
                    <Link href="/" class="btn btn-ghost text-xl">
                        Chabot IntegraCAR
                    </Link>
                </div>
                <div class="flex gap-4">
                    <Link href="/contas/cadastro" class="btn btn-ghost">Cadastrar</Link>
                    <Link href="/contas/login" class="btn btn-neutral">Entrar</Link>
                </div>
            </div>
        </div>

        <!-- Conteúdo -->
        <div class="grow">

            <slot></slot>

        </div>
    </div>
</template>
