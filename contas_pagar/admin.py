from django.contrib import admin
from .models import ContaPagar, PlanoDeContas


@admin.register(PlanoDeContas)
class PlanoDeContasAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'tipo', 'pai')
    list_filter = ('tipo',)
    search_fields = ('codigo', 'nome')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('codigo', 'nome', 'tipo')
        }),
        ('Hierarquia', {
            'fields': ('pai',)
        }),
    )


@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'fornecedor', 'valor', 'status', 'data_vencimento', 'data_pagamento')
    list_filter = ('status', 'data_vencimento', 'recorrencia')
    search_fields = ('descricao', 'fornecedor__nome')
    readonly_fields = ('criado_em', 'atualizado_em', 'recorrencia_gerada')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('descricao', 'fornecedor', 'plano_conta')
        }),
        ('Valores e Datas', {
            'fields': ('valor', 'valor_pago', 'data_emissao', 'data_vencimento', 'data_pagamento')
        }),
        ('Status e Recorrência', {
            'fields': ('status', 'recorrencia', 'quantidade_recorrencias', 'recorrencia_gerada', 'conta_origem')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('valor',)
        return self.readonly_fields
