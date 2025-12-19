<script setup lang="ts">
import { usePage, useForm, router } from '@inertiajs/vue3';

import Layout from '@/components/Layout.vue';
import type { DjangoFormData } from "@/types/djangoForm";
import type { Documento } from '@/types/index';
import { ref, watch } from 'vue';
import FormField from '@/components/form/FormField.vue';

const documentoParaExcluir = ref<Documento | null>(null);
const modalExclusao = ref<HTMLDialogElement | null>(null);

function abrirModalExclusao(documento: Documento) {
    documentoParaExcluir.value = documento;
    modalExclusao.value?.showModal();
}

function confirmarExclusao() {
    if (documentoParaExcluir.value) {
        const url = page.props['urls']['excluir_documento'].replace('%(id_documento)s', documentoParaExcluir.value.id.toString());
        router.post(url);
    }
    modalExclusao.value?.close();
    documentoParaExcluir.value = null;
}

function cancelarExclusao() {
    modalExclusao.value?.close();
    documentoParaExcluir.value = null;
}


const page = usePage<{
    urls: Record<string, string>,
}>();
const props = defineProps<{
    importar_documentos_form: DjangoFormData,
    documentos: Documento[];
    documentos_processados: number;
    documentos_pendentes: number;
}>();

const documentos = ref([...props.documentos]);
const qtdDocumentosProcessados = ref(props.documentos_processados);
const qtdDocumentosPendentes = ref(props.documentos_pendentes);

watch(
    () => ({
        docs: props.documentos,
        proc: props.documentos_processados,
        pend: props.documentos_pendentes
    }),
    (v) => {
        documentos.value = [...v.docs];
        qtdDocumentosProcessados.value = v.proc;
        qtdDocumentosPendentes.value = v.pend;
        atualizarStatusDocumentosPendentes();
    }
);

let verificando = false;
async function atualizarStatusDocumentosPendentes() {
    if (verificando) return;
    verificando = true;

    while (true) {
        const pendentes = documentos.value.filter(d => d.status === "pendente");
        if (pendentes.length === 0) break;

        await new Promise(r => setTimeout(r, 5000));

        await Promise.all(
            pendentes.map(async doc => {
                try {
                    const res = await fetch(`/api/documentos/${doc.id}/status`);
                    if (!res.ok) return;
                    const data = await res.json();
                    doc.status = data.status;
                } catch (e) {
                    console.error(e);
                }
            })
        );

        qtdDocumentosProcessados.value = documentos.value.filter(d => d.status === 'processado').length;
        qtdDocumentosPendentes.value = documentos.value.filter(d => d.status === 'pendente').length;
    }

    verificando = false;
}

atualizarStatusDocumentosPendentes();

const form = useForm({
    documentos: [],
    tipo: '',
})
function submit() {
    form.post(page.props['urls']['documentos']);
}

</script>

<template>
    <Layout>
        <div class="max-w-3xl mx-auto space-y-4 p-4">
            <div class="flex flex-col md:flex-row gap-4">
                <div class="mx-auto p-2 w-full max-w-96 rounded bg-base-300 flex flex-col items-center justify-center">
                    <p class="label">Documentos processados</p>
                    <p class="font-bold text-2xl">{{ qtdDocumentosProcessados }}</p>
                </div>
                <div class="mx-auto p-2 w-full max-w-96 rounded bg-base-300 flex flex-col items-center justify-center">
                    <p class="label">Documentos pendentes</p>
                    <p class="font-bold text-2xl">{{ qtdDocumentosPendentes }}</p>
                </div>
                <div class="mx-auto p-2 w-full max-w-96 rounded bg-base-300">
                    <form @submit.prevent="submit" class="">
                        <div class="flex gap-2 items-center">
                            <div>
                                <FormField :field="importar_documentos_form.fields[0]"
                                    @input="form.documentos = Array.from($event.target.files)" />

                                <!-- <FormField :field="importar_documentos_form.fields[1]" @input="form.tipo = $event.target.value" /> -->
                            </div>
                            <button class="btn px-2 h-14 rounded">
                                <i class="bi bi-plus-lg "></i>
                            </button>
                        </div>
                    </form>
                </div>
            </div>


            <div class="overflow-scroll">
                <table class="table table-auto">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Documento</th>
                            <th>Status</th>
                            <th>Tipo do Documento</th>
                            <th class="w-0 whitespace-nowrap">Ações</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for="documento in documentos" :key="documento.id">
                            <td>{{ documento.id }}</td>
                            <td>{{ documento.nome }}</td>
                            <td>{{ documento.status }}</td>
                            <td>{{ documento.tipo_documento }}</td>
                            <td class="w-0 whitespace-nowrap">
                                <div class="flex gap-2 justify-center">
                                    <a :href="documento.arquivo.url" target="_blank">
                                        <i class="bi bi-eye-fill text-neutral"></i>
                                    </a>
                                    <button @click="abrirModalExclusao(documento)" class="cursor-pointer">
                                        <i class="bi bi-trash3-fill text-error"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>

            <!-- Modal de confirmação de exclusão -->
            <dialog ref="modalExclusao" class="modal">
                <div class="modal-box">
                    <h3 class="font-bold text-lg">Confirmar exclusão</h3>
                    <p class="py-4">
                        Tem certeza que deseja excluir o documento
                        <strong>{{ documentoParaExcluir?.nome }}</strong>?
                    </p>
                    <div class="modal-action">
                        <button class="btn" @click="cancelarExclusao">Cancelar</button>
                        <button class="btn btn-error" @click="confirmarExclusao">Excluir</button>
                    </div>
                </div>
                <form method="dialog" class="modal-backdrop">
                    <button @click="cancelarExclusao">close</button>
                </form>
            </dialog>
        </div>
    </Layout>
</template>
