<script setup lang="ts">
import { usePage } from '@inertiajs/vue3';
import CadastrarCanonica from './CadastrarCanonica.vue';

const page = usePage();
</script>

<template>
  <CadastrarCanonica
    :form="page.props.form"
    :action-url="page.props.urls.atualizar"
    method="post"
    titulo="Editar Pergunta Canônica"
    :voltar-url="page.props.urls.curadoria"
  />
</template>
