<script setup lang="ts">
const props = defineProps<{ mensagem: string }>();
import markdownit from 'markdown-it';

const md = markdownit();
console.log(md.render(props.mensagem));

</script>

<template>
    <div class="flex flex-col items-start gap-2 mt-4 group text-black">

        <div v-if="mensagem" class="markdown" v-html="md.render(mensagem)"></div>
        <div v-else class="inline-grid *:[grid-area:1/1]">
            <div class="status status-warning animate-ping status-lg"></div>
            <div class="status status-warning status-lg"></div>
        </div>

        <div class="flex gap-0">
            <div class="flex items-center gap-0.5">
                <button class="btn btn-ghost btn-xs btn-square">
                    <i class="bi bi-caret-left text-base"></i>
                </button>
                <span class="text-sm h-fit">1/2</span>
                <button class="btn btn-ghost btn-xs btn-square">
                    <i class="bi bi-caret-right text-base"></i>
                </button>
            </div>
            <button class="btn btn-ghost btn-xs btn-square">
                <i class="bi bi-copy text-base"></i>
            </button>
            <button class="btn btn-ghost btn-xs btn-square">
                <i class="bi bi-hand-thumbs-up text-base"></i>
            </button>
            <button class="btn btn-ghost btn-xs btn-square">
                <i class="bi bi-hand-thumbs-down text-base"></i>
            </button>
            <button class="btn btn-ghost btn-xs btn-square">
                <i class="bi bi-arrow-repeat text-base"></i>
            </button>
        </div>
    </div>
</template>