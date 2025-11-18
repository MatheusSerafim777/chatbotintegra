from django import forms
from django.contrib.auth.forms import AuthenticationForm
from contas.models import Usuario
from django.contrib.auth.forms import SetPasswordMixin

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


class CadastroForm(forms.ModelForm, SetPasswordMixin):
    class Meta:
        model = Usuario
        fields = ['name', 'email']

    password1, password2 = SetPasswordMixin.create_password_fields()
    password1.required = True
    password2.required = True

    def __init__(self, *args, **kwargs):
        kwargs['use_required_attribute'] = False
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['icon'] = "bi bi-person"
        self.fields['email'].widget.attrs['icon'] = 'bi bi-envelope-fill'
        self.fields['password1'].widget.attrs['icon'] = 'bi bi-key-fill'
        self.fields['password2'].widget.attrs['icon'] = 'bi bi-key-fill'


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            self.add_error('email', 'Email já cadastrado.')
        return email

    def clean(self):
        self.validate_passwords()
        return super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        user = self.set_password_and_save(user, commit=commit)
        return user

