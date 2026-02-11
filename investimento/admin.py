from django.contrib import admin
from .models import Investimento


@admin.register(Investimento)
class InvestimentoAdmin(admin.ModelAdmin):
    list_display = [
        'data_operacao',
        'tipo_operacao',
        'tipo_ativo',
        'ticker',
        'nome_ativo',
        'quantidade',
        'preco_unitario',
        'valor_total',
        'empresa'
    ]
    
    list_filter = [
        'tipo_ativo',
        'tipo_operacao',
        'empresa',
        'data_operacao'
    ]
    
    search_fields = [
        'ticker',
        'nome_ativo',
        'observacoes'
    ]
    
    date_hierarchy = 'data_operacao'
    
    fieldsets = (
        ('Informações do Ativo', {
            'fields': (
                'empresa',
                'tipo_ativo',
                'ticker',
                'nome_ativo'
            )
        }),
        ('Dados da Operação', {
            'fields': (
                'tipo_operacao',
                'data_operacao',
                'quantidade',
                'preco_unitario',
                'valor_total'
            )
        }),
        ('Custos e Taxas', {
            'fields': (
                'taxa_corretagem',
                'taxa_custodia',
                'emolumentos',
                'impostos',
                'outras_taxas'
            ),
            'classes': ('collapse',)
        }),
        ('Informações Adicionais', {
            'fields': (
                'data_vencimento',
                'rentabilidade_contratada',
                'observacoes'
            ),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = []
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editando
            return ['criado_em', 'atualizado_em']
        return []
