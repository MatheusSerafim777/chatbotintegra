
<script setup lang="ts">
import { Form } from '@inertiajs/vue3';
import { Link } from '@inertiajs/vue3';

import type { DjangoFormData } from "@/types/djangoForm";

import DjangoForm from '@/components/form/DjangoForm.vue'

defineProps<{ form: DjangoFormData }>();


</script>
<template>
    <div class="flex h-screen items-center justify-center bg-base-200 ">
        <div class="card bg-base-100 card-border border-base-300 card-sm overflow-hidden min-w-xs sm:min-w-sm">
            <div class="border-base-300 border-b border-dashed">
                <div class="flex items-center gap-2 p-4">
                    <div class="grow">
                        <div class="flex items-center gap-2 text-sm font-medium">
                            <i class="bi bi-person text-xl"></i>
                            Cadastrar
                        </div>
                    </div>
                </div>
            </div>
            <Form action="/contas/cadastro/" method="post" class="card-body gap-4">
                <p class="text-xs opacity-60">Faça seu cadastro</p>

                <DjangoForm :form="form" />


                <label class="text-base-content/60 flex items-center gap-2 text-xs">
                    <input name="remember" type="checkbox" class="toggle toggle-xs" checked>
                    Lembrar de mim
                </label>
                <div class="card-actions flex flex-col items-center justify-center gap-6">
                    <button class="btn btn-neutral">Cadastrar</button>
                    <Link href="/contas/login/">Ja tem conta?</Link>
                </div>
            </Form>

        </div>
    </div>
</template>