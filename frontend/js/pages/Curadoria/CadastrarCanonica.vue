<script setup lang="ts">
import { ref } from 'vue';
import Layout from '@/components/Layout.vue';
import { usePage, Form, Link } from '@inertiajs/vue3';
import markdownit from 'markdown-it';
import DjangoForm from '@/components/form/DjangoForm.vue'
import { DjangoFormData } from '@/types/djangoForm';
import FormField from '@/components/form/FormField.vue';

FormField
defineProps<{ form: DjangoFormData }>();

const page = usePage();

const md = markdownit();

const resposta = ref('');

</script>


<template>
    <Layout>
        <Link class="btn m-4 w-fit" :href="page.props['urls']['curadoria']"><i class="bi bi-box-arrow-in-left"></i>Voltar</Link>
        <div class="max-w-3xl mx-auto space-y-4 p-4 w-full">

            <div class="max-w-5xl mx-auto">

                <Form :action="page.props['urls']['cadastro_canonica']" method="post">
                    <div class="flex flex-col gap-4 p-4">
                        <div>
                            <FormField :field="form.fields[0]"/>
                        </div>
                        <div class="flex gap-5">

                            <div class="w-full">
                                <FormField :field="form.fields[1]" @input="resposta = $event.target.value"/>
                            </div>

                            <div class="w-full">
                                <h3>Resposta Renderizada:</h3>
                                <div v-html="md.render(resposta)"
                                    class="markdown border border-b-base-content rounded-4xl p-2 h-full"></div>
                            </div>

                        </div>
                        <button class="btn btn-primary mt-6 w-fit" type="submit">Cadastrar</button>
                    </div>
                </Form>

            </div>
        </div>
    </Layout>
</template>
