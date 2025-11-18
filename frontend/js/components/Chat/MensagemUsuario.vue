<script setup lang="ts">
defineProps<{ mensagem: string }>();
</script>

<template>
    <div class="flex flex-col items-end gap-2 group">
        <div class="max-w-lg p-4 rounded-2xl bg-base-200">
            {{ mensagem }}
        </div>
        <div
            class="flex gap-0 opacity-0 pointer-events-none transition group-hover:opacity-100 group-hover:pointer-events-auto">
            <button class="btn btn-ghost btn-xs btn-square">
                <i class="bi bi-copy text-base"></i>
            </button>
            <button class="btn btn-ghost btn-xs btn-square">
                <i class="bi bi-pencil text-base"></i>
            </button>
            <div class="flex items-center gap-0.5">
                <button class="btn btn-ghost btn-xs btn-square">
                    <i class="bi bi-caret-left text-base"></i>
                </button>
                <span class="text-sm h-fit">1/2</span>
                <button class="btn btn-ghost btn-xs btn-square">
                    <i class="bi bi-caret-right text-base"></i>
                </button>
            </div>
        </div>
    </div>
</template>