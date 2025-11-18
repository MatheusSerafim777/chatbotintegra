<script setup lang="ts">
import type { FormField } from "@/types/djangoForm";

const props = defineProps<{ field: FormField }>();

// remove o atributo icon antes de passar ao input
const attrs = { ...props.field.widget_attrs };
delete attrs.icon;
</script>

<template>
    <label 
        class="input input-bordered flex items-center gap-2 w-full"
        :class="{ 'input-error': field.errors.length }"
    >
        <i :class="field.widget_attrs.icon" class="text-xl"></i>

        <input
            class="grow"
            :type="field.input_type || 'text'"
            :id="field.id_for_label"
            :name="field.name"
            :value="field.value"
            :disabled="field.disabled"
            autocomplete="off"
            v-bind="attrs"
        />
    </label>
</template>
