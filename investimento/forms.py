from django import forms
from .models import Investimento
from decimal import Decimal, InvalidOperation


class InvestimentoForm(forms.ModelForm):
    # Campos de valor com máscara
    preco_unitario = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control money'})
    )
    valor_total = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control money'})
    )
    taxa_corretagem = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control money'})
    )
    taxa_custodia = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control money'})
    )
    emolumentos = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control money'})
    )
    impostos = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control money'})
    )
    outras_taxas = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control money'})
    )
    quantidade = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control money'})
    )

    class Meta:
        model = Investimento
        fields = [
            'empresa',
            'tipo_ativo',
            'ticker',
            'nome_ativo',
            'tipo_operacao',
            'data_operacao',
            'quantidade',
            'preco_unitario',
            'valor_total',
            'taxa_corretagem',
            'taxa_custodia',
            'emolumentos',
            'impostos',
            'outras_taxas',
            'data_vencimento',
            'rentabilidade_contratada',
            'observacoes',
        ]

    def clean_valor(self, field_name):
        """Converte valor formatado (1.234,56) para Decimal"""
        val = self.cleaned_data.get(field_name)
        if val in (None, ''):
            return Decimal('0.00')
        if isinstance(val, Decimal):
            return val
        if isinstance(val, str):
            normalized = val.replace('.', '').replace(',', '.')
            try:
                return Decimal(normalized)
            except (InvalidOperation, ValueError):
                raise forms.ValidationError('Valor inválido')
        return Decimal('0.00')

    def clean_preco_unitario(self):
        return self.clean_valor('preco_unitario')

    def clean_valor_total(self):
        return self.clean_valor('valor_total')

    def clean_taxa_corretagem(self):
        return self.clean_valor('taxa_corretagem')

    def clean_taxa_custodia(self):
        return self.clean_valor('taxa_custodia')

    def clean_emolumentos(self):
        return self.clean_valor('emolumentos')

    def clean_impostos(self):
        return self.clean_valor('impostos')

    def clean_outras_taxas(self):
        return self.clean_valor('outras_taxas')

    def clean_quantidade(self):
        return self.clean_valor('quantidade')
