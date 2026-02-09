from django.contrib import admin
from .models import ContaReceber


@admin.register(ContaReceber)
class ContaReceberAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'cliente', 'valor', 'status', 'data_vencimento', 'data_recebimento')
    list_filter = ('status', 'data_vencimento')
    search_fields = ('descricao', 'cliente__nome')
    readonly_fields = ('criado_em', 'atualizado_em')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('descricao', 'cliente')
        }),
        ('Valores e Datas', {
            'fields': ('valor', 'valor_recebido', 'data_emissao', 'data_vencimento', 'data_recebimento')
        }),
        ('Status', {
            'fields': ('status',)
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
