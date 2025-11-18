<script setup lang="ts">
import type { DjangoFormData } from '@/types/djangoForm';
import FormField from './FormField.vue'

defineProps<{ form: DjangoFormData }>();
</script>

<template>
    <!-- Non-field errors -->
    <div v-if="form.non_field_errors.length" class="space-y-2">
        <div v-for="(error, i) in form.non_field_errors" :key="i" class="alert alert-error flex items-center gap-2">
            <i class="bi bi-exclamation-triangle-fill"></i>
            <span>{{ error }}</span>
        </div>
    </div>

    <!-- Fields -->
    <FormField v-for="field in form.fields" :key="field.name" :field="field" />
</template>
