<script setup lang="ts">
import { Link, usePage, Form } from '@inertiajs/vue3';

import type { DjangoFormData } from "@/types/djangoForm";
import LayoutAnonimo from '@/components/LayoutAnonimo.vue';

import DjangoForm from '@/components/form/DjangoForm.vue'

defineProps<{ form: DjangoFormData }>();

const page = usePage<{
    urls: Record<string, string>,
}>();
</script>


<template>
    <LayoutAnonimo>
        <div class="flex grow min-h-0 items-center justify-center py-4 sm:py-8">
            <div class="card bg-base-200 card-border border-base-300 card-sm w-full max-w-md">
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
                <Form :action="page.props.urls['cadastrar']" method="post" class="card-body gap-4">
                    <p class="text-xs opacity-60">Faça seu cadastro</p>

                    <DjangoForm :form="form" />


                    <label class="text-base-content/60 flex items-center gap-2 text-xs">
                        <input name="remember" type="checkbox" class="toggle toggle-xs" checked>
                        Lembrar de mim
                    </label>

                    <div class="card-actions flex flex-col items-center justify-center gap-4">
                        <button class="btn btn-neutral btn-block">Cadastrar</button>
                        <Link :href="page.props.urls['entrar']" class="link link-hover">Já tem conta? Entrar</Link>
                    </div>
                </Form>

            </div>
        </div>
    </LayoutAnonimo>
</template>