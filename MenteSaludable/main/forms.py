from django import forms
from .models import Pregunta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_bootstrap5.bootstrap5 import FloatingField


class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        preguntas = kwargs.pop('preguntas')
        super().__init__(*args, **kwargs)
        
        for pregunta in preguntas:
            self.fields[f'pregunta_{pregunta.id}'] = forms.ChoiceField(
                label=pregunta.texto,
                choices=[(i, str(i)) for i in range(1, 6)],
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                help_text=f"Categoría: {pregunta.get_categoria_display()}"
            )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrarse'))
