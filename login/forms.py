from django.contrib.auth.forms import AuthenticationForm
from django import forms


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Usuário",
            "autofocus": True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Senha"
        })
    )
