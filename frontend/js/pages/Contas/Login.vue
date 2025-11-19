<script setup lang="ts">
import { Form } from '@inertiajs/vue3';
import { Link } from '@inertiajs/vue3';
import type { DjangoFormData } from "@/types/djangoForm";
import LayoutAnonimo from '@/components/LayoutAnonimo.vue';

import DjangoForm from '@/components/form/DjangoForm.vue'

defineProps<{ form: DjangoFormData }>();
</script>

<template>
    <LayoutAnonimo>

        <div class="flex h-screen items-center justify-center">
            <div class="card card-sm overflow-hidden min-w-xs sm:min-w-sm">
                <div class="card bg-base-200 card-border border-base-300 card-sm overflow-hidden ">
                    <div class="border-base-300 border-b border-dashed">
                        <div class="flex items-center gap-2 p-4">
                            <div class="grow">
                                <div class="flex items-center gap-2 text-sm font-medium">
                                    <i class="bi bi-person text-xl"></i>
                                    Entrar
                                </div>
                            </div>
                        </div>
                    </div>
                    <Form action="/contas/login/" method="post" class="card-body gap-4">
                        <p class="text-xs opacity-60">Digite suas credenciais para acessar sua conta</p>

                        <DjangoForm :form="form" />

                        <label class="text-base-content/60 flex items-center gap-2 text-xs">
                            <input name="remember" type="checkbox" class="toggle toggle-xs" checked>
                            Lembrar de mim
                        </label>
                        <div class="card-actions flex items-center justify-center gap-6 flex-col">
                            <button class="btn btn-neutral">Entrar</button>
                            <Link href="/contas/cadastro/">Não tem conta? Cadastrar</Link>
                        </div>
                    </Form>
                </div>
            </div>
        </div>
    </LayoutAnonimo>
</template>
