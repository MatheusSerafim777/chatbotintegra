from chat.models import RespostaCanonica
from django import forms


class RespostaCanonicaForm(forms.ModelForm):
    class Meta:
        model = RespostaCanonica
        fields = [
            'pergunta',
            'resposta',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['pergunta'].widget.attrs.update({'rows': 1})
        self.fields['resposta'].widget.attrs.update({'rows': 5})
