from django.db.models.fields.files import FieldFile
from django.forms import BaseModelForm, Form, ModelForm
from inertia.utils import InertiaJsonEncoder


class CustomJsonEncoder(InertiaJsonEncoder):
    def _form_encoder(self, form: BaseModelForm):
        fields = []

        for bound_field in form:
            field = bound_field.field
            widget = field.widget

            # Value sempre string (evita None e listas inesperadas)
            raw_value = bound_field.value()
            if raw_value is None:
                value = ''
            elif isinstance(raw_value, (list, tuple)):
                value = list(raw_value)
            else:
                value = str(raw_value)

            choices = []
            if hasattr(field, 'choices'):
                choices = field.choices

            fields.append({
                'name': bound_field.name,
                'label': bound_field.label or '',
                'help_text': bound_field.help_text or '',
                'errors': list(bound_field.errors),
                'value': value,
                'input_type': getattr(widget, 'input_type', None),
                'widget_type': widget.__class__.__name__,
                'id_for_label': bound_field.id_for_label,
                # garante dict mesmo se attrs for None
                'widget_attrs': widget.attrs.copy() if widget.attrs else {},
                # informações extras úteis no front
                'required': field.required,
                'disabled': field.disabled,
                'hidden': widget.is_hidden,
                'choices': choices,
            })

        return {
            'fields': fields,
            'non_field_errors': list(form.non_field_errors()),
            'is_valid': form.is_bound and form.is_valid(),
        }

    def _file_field_encoder(self, field: FieldFile):
        if not field:
            return None
        return {
            'name': field.name,
            'url': field.url,
        }

    def default(self, obj):
        if isinstance(obj, (ModelForm, Form)):
            return self._form_encoder(obj)
        if isinstance(obj, FieldFile):
            return self._file_field_encoder(obj)

        return super().default(obj)
