<script setup lang="ts">
import type { FormField } from "@/types/djangoForm";
defineProps<{ field: FormField }>();
</script>

<template>
    <input :class="[
        field.input_type !== 'file' && 'input',
        'w-full',
        field.errors.length && 'input-error',
        field.input_type === 'file' && 'file-input'
    ]" :type="field.input_type || 'text'" :id="field.id_for_label" :name="field.name" :value="field.value"
        :disabled="field.disabled" v-bind="field.widget_attrs" />

</template>
