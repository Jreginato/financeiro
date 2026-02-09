from django import forms
from .models import ContaPagar, PlanoDeContas
from decimal import Decimal, InvalidOperation


class PlanoDeContasForm(forms.ModelForm):
    class Meta:
        model = PlanoDeContas
        fields = [
            "codigo",
            "nome",
            "tipo",
            "pai",
        ]
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "pai": forms.Select(attrs={"class": "form-control select2"}),
        }


class ContaPagarForm(forms.ModelForm):
    # tratamos o campo `valor` como CharField no form para aceitar máscaras (ex: "1.234,56")
    valor = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control money'}))
    class Meta:
        model = ContaPagar
        fields = [
            "descricao",
            "fornecedor",
            "plano_conta",
            "valor",
            "data_emissao",
            "data_vencimento",
            "status",
            "recorrencia",
            "quantidade_recorrencias",
            "observacoes",
        ]
        widgets = {
            # outros widgets mantidos pelo template via filter `add_class`
        }

    def clean(self):
        cleaned = super().clean()

        recorrencia = cleaned.get("recorrencia")
        qtd = cleaned.get("quantidade_recorrencias")

        if recorrencia != ContaPagar.Recorrencia.NENHUMA and not qtd:
            self.add_error("quantidade_recorrencias", "Informe quantos lançamentos deseja gerar.")

        return cleaned

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
        # fallback
        try:
            return Decimal(val)
        except Exception:
            raise forms.ValidationError('Valor inválido')