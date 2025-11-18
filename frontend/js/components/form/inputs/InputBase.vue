<script setup lang="ts">
import type { FormField } from "@/types/djangoForm";
defineProps<{ field: FormField }>();
</script>

<template>
    <input class="input input-bordered w-full" :class="{ 'input-error': field.errors.length }"
        :type="field.input_type || 'text'" :id="field.id_for_label" :name="field.name" :value="field.value"
        :disabled="field.disabled" v-bind="field.widget_attrs" />
</template>
