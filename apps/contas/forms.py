from django import forms
from django.contrib.auth.forms import AuthenticationForm


class FormSeriazableMixin:
    def as_dict(self):
        return {name: field.value() for name, field in self.fields.items()}


class SigninForm(AuthenticationForm):
    def get_invalid_login_error(self):
        return forms.ValidationError('Credenciais inválidas.')

    def __init__(self, *args, **kwargs):
        kwargs['use_required_attribute'] = False
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['autofocus'] = False

        self.fields['username'].widget.attrs['icon'] = 'bi bi-envelope-fill'
        self.fields['password'].widget.attrs['icon'] = 'bi bi-key-fill'

        placeholders = {
            'username': 'Email',
            'password': 'Senha',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = placeholders[field_name]
