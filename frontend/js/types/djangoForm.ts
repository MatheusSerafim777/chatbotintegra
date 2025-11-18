export type FormField = {
    name: string;
    label: string;
    help_text: string;
    errors: string[];
    value: string | string[];
    input_type: string | null;
    widget_type: string;
    id_for_label: string;
    widget_attrs: Record<string, string>;
    required: boolean;
    disabled: boolean;
    hidden: boolean;
}

export type DjangoFormData = {
    fields: FormField[];
    non_field_errors: string[];
    is_valid: boolean;
}