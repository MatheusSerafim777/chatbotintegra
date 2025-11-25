<script setup lang="ts">
import { usePage, Form } from '@inertiajs/vue3';

import Layout from '@/components/Layout.vue';
import type { DjangoFormData } from "@/types/djangoForm";
import DjangoForm from '@/components/form/DjangoForm.vue'


const page = usePage();
defineProps<{ importar_documentos_form: DjangoFormData }>();

</script>

<template>
    <Layout>
        <div class="max-w-3xl p-4">
            <div class="mx-auto p-2 max-w-80 rounded bg-base-300">
                <Form :action="page.props['urls']['documentos']" method="post" class="flex gap-2 items-center">
                    <DjangoForm :form="importar_documentos_form" />
                    <button class="btn px-2 h-14 rounded">
                        <i class="bi bi-plus-lg "></i>
                    </button>
                </Form>
            </div>
        </div>
    </Layout>
</template>
