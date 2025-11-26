<script setup lang="ts">
import { usePage, Form, Link } from '@inertiajs/vue3';

import Layout from '@/components/Layout.vue';
import type { DjangoFormData } from "@/types/djangoForm";
import type { Documento } from '@/types/index';
import DjangoForm from '@/components/form/DjangoForm.vue'
import { ref, watch } from 'vue';


const page = usePage();
const props = defineProps<{
    importar_documentos_form: DjangoFormData,
    documentos: Documento[];
    documentos_processados: number;
    documentos_pendentes: number;
}>();

const documentos = ref<Documento[]>( props.documentos);
const qtdDocumentosProcessados = ref<number>(props.documentos_processados);
const qtdDocumentosPendentes = ref<number>(props.documentos_pendentes);

watch(() => props.documentos, (v) => {
    documentos.value = v;
})
watch(() => props.documentos_processados, (v) => {
    qtdDocumentosProcessados.value = v;
})
watch(() => props.documentos_pendentes, (v) => {
    qtdDocumentosPendentes.value = v;
})


async function atualizarStatusDocumentos(documentosPendentes: Documento[]) {
    await new Promise(resolve => setTimeout(resolve, 5000));
    for (const doc of documentos.value) {
        try {
            const res = await fetch(`/api/documentos/${doc.id}/status`);
            if (res.ok) {
                const data = await res.json();
                doc.status = data.status;
                qtdDocumentosProcessados.value = documentos.value.filter((doc) => doc.status == 'processado').length;
                qtdDocumentosPendentes.value = documentos.value.filter((doc) => doc.status == 'pendente').length;
            } else {
                console.error(`Erro ao obter status do documento ${doc.id}: ${res.statusText}`);
            }
        } catch (error) {
            console.error(`Erro ao fazer requisição para documento ${doc.id}: ${error}`);
        }
    }
    documentosPendentes = documentosPendentes.filter((doc) => doc.status == 'pendente');
    if (documentosPendentes.length > 0) {
        atualizarStatusDocumentos(documentosPendentes);
    }
};

const documentosPendentes = documentos.value.filter((doc) => doc.status == 'pendente');
atualizarStatusDocumentos(documentosPendentes);
</script>

<template>
    <Layout>
        <div class="max-w-3xl mx-auto space-y-4 p-4">
            <div class="flex gap-4">
                <div class="mx-auto p-2 w-full max-w-96 rounded bg-base-300">
                    <p class="label text-center">Documentos processados</p>
                    <p class="font-bold text-2xl text-center">{{ qtdDocumentosProcessados }}</p>
                </div>
                <div class="mx-auto p-2 w-full max-w-96 rounded bg-base-300">
                    <p class="label text-center">Documentos pendentes</p>
                    <p class="font-bold text-2xl text-center">{{ qtdDocumentosPendentes }}</p>
                </div>
                <div class="mx-auto p-2 w-full max-w-96 rounded bg-base-300">
                    <Form :action="page.props['urls']['documentos']" method="post" class="flex gap-2 items-center">
                        <DjangoForm :form="importar_documentos_form" />
                        <button class="btn px-2 h-14 rounded">
                            <i class="bi bi-plus-lg "></i>
                        </button>
                    </Form>
                </div>
            </div>


            <div class="overflow-scroll">
                <table class="table table-auto">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Documento</th>
                            <th>Status</th>
                            <th class="w-0 whitespace-nowrap">Ações</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for="documento in documentos" :key="documento.id">
                            <td>{{ documento.id }}</td>
                            <td>{{ documento.nome }}</td>
                            <td>{{documento.status}}</td>
                            <td class="w-0 whitespace-nowrap">
                                <div class="flex gap-2 justify-center">
                                    <a :href="documento.arquivo.url" target="_blank">
                                        <i class="bi bi-eye-fill text-neutral"></i>
                                    </a>
                                    <Link :href="page.props['urls']['excluir_documento'].replace('%(id)s', documento.id)" method="post">
                                        <i class="bi bi-trash3-fill text-error"></i>
                                    </Link>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>
        </div>
    </Layout>
</template>
