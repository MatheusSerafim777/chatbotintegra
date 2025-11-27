<script setup lang="ts">

import Layout from '@/components/Layout.vue';
import DjangoForm from '@/components/form/DjangoForm.vue'

import { usePage, Form, Link } from '@inertiajs/vue3';
import type { DjangoFormData } from "@/types/djangoForm";
import type { Documento } from '@/types/index';
import { ref, watch } from 'vue';

const page = usePage();
</script>


<template>
    <Layout>
        <div class="max-w-3xl mx-auto space-y-4 p-4">

            <div class="overflow-scroll">
                <Link class="btn btn-primary mb-4" :href="page.props['urls']['cadastro_canonica']">Inserir</Link>

                <div class="flex flex-col gap-3">
                    
                    <div class="collapse bg-base-100 border border-base-300">
                        <input type="radio" name="my-accordion-1"/>
                        <div class="collapse-title font-semibold flex justify-between p-4">
                            <span>Pergunta 1</span>
                            <div class="flex gap-2">
                                <Link method="post"><i class="bi bi-trash3-fill text-error"></i></Link>
                                <Link method="post"><i class="bi bi-pencil"></i></Link>
                            </div>
                        </div>
                        <div class="collapse-content text-sm">Resposta 1</div>
                    </div>
                    <div class="collapse bg-base-100 border border-base-300">
                        <input type="radio" name="my-accordion-1" />
                        <div class="collapse-title font-semibold flex justify-between p-4">
                            <span>Pergunta 2</span>
                            <div class="flex gap-2">
                                <Link method="post"><i class="bi bi-trash3-fill text-error"></i></Link>
                                <Link method="post"><i class="bi bi-pencil"></i></Link>
                            </div>

                        </div>
                        <div class="collapse-content text-sm">Respota 2</div>
                    </div>
                    <div class="collapse bg-base-100 border border-base-300">
                        <input type="radio" name="my-accordion-1" />
                        <div class="collapse-title font-semibold flex justify-between p-4">
                            <span>Pergunta 3</span>
                            <div class="flex gap-2">
                                <Link method="post"><i class="bi bi-trash3-fill text-error"></i></Link>
                                <Link method="post"><i class="bi bi-pencil"></i></Link>
                            </div>
                        </div>
                        <div class="collapse-content text-sm">Resposta 3</div>
                    </div>

                </div>


            </div>
        </div>
    </Layout>
</template>