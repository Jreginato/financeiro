from django import forms
from .models import Assinatura
from decimal import Decimal, InvalidOperation


class AssinaturaForm(forms.ModelForm):
    valor = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control money'})
    )

    class Meta:
        model = Assinatura
        fields = [
            "descricao",
            "fornecedor",
            "plano_conta",
            "valor",
            "periodicidade",
            "dia_vencimento",
            "data_inicio",
            "data_cancelamento",
            "status",
            "observacoes",
        ]
        widgets = {
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "fornecedor": forms.Select(attrs={"class": "form-control select2"}),
            "plano_conta": forms.Select(attrs={"class": "form-control select2"}),
            "periodicidade": forms.Select(attrs={"class": "form-control"}),
            "dia_vencimento": forms.NumberInput(attrs={"class": "form-control", "min": "1", "max": "28"}),
            "data_inicio": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "data_cancelamento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean_valor(self):
        val = self.cleaned_data.get('valor')
        if val in (None, ''):
            return val
        if isinstance(val, Decimal):
            return val
        if isinstance(val, str):
            normalized = val.replace('.', '').replace(',', '.')
            try:
                return Decimal(normalized)
            except InvalidOperation:
                raise forms.ValidationError('Valor inválido')
        try:
            return Decimal(val)
        except Exception:
            raise forms.ValidationError('Valor inválido')
