<script setup lang="ts">
import { Link } from '@inertiajs/vue3';
</script>
<template>
    <div class="min-h-screen flex flex-col">
        <!-- Navbar fixa -->
        <div class="bg-base-100 shadow-sm sticky top-0 z-20">
            <div class="navbar mx-auto max-w-3xl">
                <div class="flex-1">
                    <a class="btn btn-ghost text-xl">
                        Chabot IntegraCAR
                    </a>
                </div>
                <div class="flex-none">
                    <Link href="/contas/login" class="btn btn-neutral">
                    Entrar
                    </Link>
                </div>
            </div>
        </div>

        <!-- Conteúdo -->
        <div class="p-4 grow">

            <slot></slot>

        </div>
    </div>
</template>
