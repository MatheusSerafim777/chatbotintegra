<script setup lang="ts">
defineProps<{ mensagem: string }>();

function escapeHtml(str: string): string {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;")
        .replace(/\n/g, '<br>');
}

</script>

<template>
    <div class="flex flex-col items-end gap-2 group">
        <div
            class="max-w-lg px-4 py-1.5 rounded-[18px] bg-neutral text-neutral-content whitespace-pre-wrap wrap-break-word">
            <p v-html="escapeHtml(mensagem)"></p>
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