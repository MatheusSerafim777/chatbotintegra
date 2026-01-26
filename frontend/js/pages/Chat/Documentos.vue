<script setup lang="ts">
import { usePage, router } from '@inertiajs/vue3';

import Layout from '@/components/Layout.vue';
import type { DjangoFormData } from "@/types/djangoForm";
import type { Documento } from '@/types/index';
import { ref, watch } from 'vue';

const documentoParaExcluir = ref<Documento | null>(null);
const modalExclusao = ref<HTMLDialogElement | null>(null);
const modalImportacao = ref<HTMLDialogElement | null>(null);

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
    // documentoParaExcluir.value = null;
}

function abrirModalImportacao() {
    modalImportacao.value?.showModal();
}

function fecharModalImportacao() {
    modalImportacao.value?.close();
    documentosParaImportar.value = [{ arquivo: null, tipo: 'manual' }];
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

type DocumentoParaImportar = {
    arquivo: File | null;
    tipo: 'manual' | 'legislacao';
};

const documentosParaImportar = ref<DocumentoParaImportar[]>([
    { arquivo: null, tipo: 'manual' }
]);

function adicionarDocumento() {
    documentosParaImportar.value.push({ arquivo: null, tipo: 'manual' });
}

function removerDocumento(index: number) {
    if (documentosParaImportar.value.length > 1) {
        documentosParaImportar.value.splice(index, 1);
    }
}

function handleFileChange(index: number, event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
        documentosParaImportar.value[index].arquivo = target.files[0];
    }
}

function submit() {
    const formData = new FormData();

    documentosParaImportar.value.forEach((doc, index) => {
        if (doc.arquivo) {
            formData.append(`documentos[${index}]`, doc.arquivo);
            formData.append(`tipos[${index}]`, doc.tipo);
        }
    });

    router.post(page.props['urls']['documentos'], formData, {
        onSuccess: () => {
            fecharModalImportacao();
        }
    });
}

async function atualizarTipoDocumento(documento: Documento, novoTipo: string) {
    try {
        const res = await fetch(`/api/documentos/${documento.id}/tipo`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ tipo: novoTipo })
        });

        if (!res.ok) {
            console.error('Erro ao atualizar tipo de documento');
        }
    } catch (e) {
        console.error(e);
    }
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
                <div class="mx-auto p-2 w-full max-w-96 rounded flex items-center justify-center">
                    <button @click="abrirModalImportacao" class="btn btn-primary">
                        <i class="bi bi-plus-lg"></i>
                        Adicionar Documentos
                    </button>
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
                            <td>{{ documento.status.charAt(0).toUpperCase() + documento.status.slice(1) }}</td>
                            <td>
                                <select v-model="documento.tipo"
                                    @change="atualizarTipoDocumento(documento, documento.tipo)"
                                    class="select select-bordered select-sm w-full max-w-xs">
                                    <option value="manual">Manual</option>
                                    <option value="legislacao">Legislação</option>
                                </select>
                            </td>
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

            <!-- Modal de importação -->
            <dialog ref="modalImportacao" class="modal">
                <div class="modal-box max-w-2xl">
                    <h3 class="font-bold text-lg mb-4">Adicionar Documentos</h3>

                    <div class="space-y-3 max-h-96 overflow-y-auto bg-base-200 rounded p-3">
                        <div v-for="(doc, index) in documentosParaImportar" :key="index"
                            class="flex gap-2 items-center">
                            <div class="flex-1">
                                <input type="file" accept=".pdf" @change="handleFileChange(index, $event)"
                                    class="file-input file-input-bordered file-input-sm w-full" />
                            </div>
                            <div class="w-40">
                                <select v-model="doc.tipo" class="select select-bordered select-sm w-full">
                                    <option value="manual">Manual</option>
                                    <option value="legislacao">Legislação</option>
                                </select>
                            </div>
                            <button v-if="documentosParaImportar.length > 1" @click="removerDocumento(index)"
                                class="btn btn-sm btn-ghost btn-circle">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>

                    <div class="mt-4">
                        <button @click="adicionarDocumento" class="btn btn-sm btn-outline w-full">
                            <i class="bi bi-plus-lg"></i>
                            Adicionar outro documento
                        </button>
                    </div>

                    <div class="modal-action">
                        <button class="btn" @click="fecharModalImportacao">Cancelar</button>
                        <button class="btn btn-primary" @click="submit">Enviar</button>
                    </div>
                </div>
                <form method="dialog" class="modal-backdrop">
                    <button @click="fecharModalImportacao">close</button>
                </form>
            </dialog>

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
