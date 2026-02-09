from django import forms
from .models import ContaReceber
from decimal import Decimal, InvalidOperation


class ContaReceberForm(forms.ModelForm):
    # tratamos o campo `valor` como CharField no form para aceitar máscaras (ex: "1.234,56")
    valor = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control money'}))

    class Meta:
        model = ContaReceber
        fields = [
            "descricao",
            "cliente",
            "valor",
            "data_emissao",
            "data_vencimento",
            "status",
            "observacoes",
        ]
        widgets = {
            # outros widgets mantidos pelo template via filter `add_class`
        }

    def clean_valor(self):
        val = self.cleaned_data.get('valor')
        if val in (None, ''):
            return val
        # If it's already a Decimal (unlikely when using TextInput), return
        if isinstance(val, Decimal):
            return val
        # Expecting a string like '1.234,56' or '1234,56' or '220'
        if isinstance(val, str):
            normalized = val.replace('.', '').replace(',', '.')
            try:
                return Decimal(normalized)
            except InvalidOperation:
                raise forms.ValidationError('Valor inválido')
