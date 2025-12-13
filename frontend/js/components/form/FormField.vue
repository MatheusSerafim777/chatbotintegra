<script setup lang="ts">
import type { FormField } from "@/types/djangoForm";

import InputBase from "./inputs/InputBase.vue";
import InputWithIcon from "./inputs/InputWithIcon.vue";
import TextareaField from "./inputs/TextareaField.vue";
import SelectInput from "./inputs/SelectInput.vue";

const props = defineProps<{ field: FormField }>();

// regras simples:
const isTextarea = props.field.widget_type === "Textarea";
const hasIcon = !!props.field.widget_attrs.icon;
</script>

<template>
    <input v-if="field.hidden" type="hidden" :name="field.name" :value="field.value" />

    <div v-else class="form-control w-full">
        <label class="label" :for="field.id_for_label">
            <span class="label-text font-medium">{{ field.label }}</span>
            <span v-if="field.required" class="text-error">*</span>
            <div v-if="field.help_text" class="tooltip tooltip-right tooltip-info" :data-tip="field.help_text">
                <i class="bi bi-info-circle text-info"></i>
            </div>
        </label>

        <InputWithIcon v-if="hasIcon" :field="field" />

        <SelectInput v-else-if="field.widget_type === 'Select'" :field="field" />

        <TextareaField v-else-if="isTextarea" :field="field" />

        <InputBase v-else :field="field" />

        <label class="label text-error" v-if="field.errors.length">
            <span class="label-text-alt whitespace-pre-wrap wrap-break-word" v-for="(error, i) in field.errors"
                :key="i">
                {{ error }}
            </span>
        </label>
    </div>
</template>
