<script setup lang="ts">
import { ref, watch } from 'vue';
import Layout from '@/components/Layout.vue';
import { usePage, Form, Link } from '@inertiajs/vue3';
import markdownit from 'markdown-it';
import { DjangoFormData } from '@/types/djangoForm';
import FormField from '@/components/form/FormField.vue';

const props = defineProps<{
    form: DjangoFormData;
    actionUrl: string;
    method?: 'post' | 'put';
    titulo: string;
    voltarUrl: string;
}>();

const page = usePage();
const md = markdownit();

const pergunta = ref(props.form.fields[0]?.value ?? '');
const resposta = ref<string>('' + (props.form.fields[1]?.value ?? ''));


const form = props.form;

function atualizarPerguntaResposta() {
    form.fields[0].value = pergunta.value;
    form.fields[1].value = resposta.value;
}

const handleRespostaUpdate = (value: any) => {
    resposta.value = String(value ?? '');
};
watch(pergunta, v => form.fields[0].value = v);
watch(resposta, v => form.fields[1].value = v);


</script>



<template>
    <Layout>
        <Link class="btn m-4 w-fit" :href="page.props['urls']['curadoria']"><i
            class="bi bi-box-arrow-in-left"></i>Voltar</Link>
        <div class="max-w-3xl mx-auto space-y-4 p-4 w-full">
            <h2 class="text-xl font-bold">{{ props.titulo }}</h2>

            <div class="max-w-5xl mx-auto">
                <Form :action="actionUrl" :method="'post'">
                    <div class="flex flex-col gap-4 p-4">

                        <FormField :field="form.fields[0]" v-model="pergunta" />

                        <div class="flex gap-5">
                            <div class="w-full">
                                <FormField
                                    :field="form.fields[1]"
                                    v-model="resposta"
                                    @update:modelValue="handleRespostaUpdate"
                                />
                            </div>

                            <div class="w-full">
                                <h3>Resposta Renderizada:</h3>
                                <div v-html="md.render(resposta)"
                                    class="markdown border border-b-base-content rounded-4xl p-2 h-full">
                                </div>
                            </div>
                        </div>

                        <button class="btn btn-primary mt-6 w-fit" type="submit" @click="atualizarPerguntaResposta" >
                            {{ props.method === 'put' ? "Salvar" : "Cadastrar" }}
                        </button>
                    </div>
                </Form>


            </div>
        </div>
    </Layout>
</template>