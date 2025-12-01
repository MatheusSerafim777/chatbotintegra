<script setup lang="ts">
import { ref } from 'vue';
import Layout from '@/components/Layout.vue';
import { usePage, Form, Link } from '@inertiajs/vue3';
import markdownit from 'markdown-it';

const page = usePage();

const md = markdownit();

const resposta = ref<string>('');

</script>


<template>
    <Layout>
        <div class="max-w-3xl mx-auto space-y-4 p-4 w-full">
            <Link class="btn m-4" :href="page.props['urls']['curadoria']"><i class="bi bi-box-arrow-in-left"></i>Voltar
            </Link>

            <div class="max-w-5xl mx-auto">
                <Form>
                    <div class="flex flex-col gap-4 p-4">
                        <div>
                            <label for="pergunta">Pergunta: </label><br>
                            <input type="text" id="pergunta" placeholder="Pergunta" class="input w-full">
                        </div>
                        <div class="flex gap-5">

                            <div class="w-full">
                                <label for="resposta">Resposta: </label><br>
                                <textarea type="text" id="resposta" placeholder="Escreva a resposta em Markdown"
                                    class="textarea w-full h-full" v-model="resposta"></textarea>
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
