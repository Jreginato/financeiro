from django.contrib import admin
from .models import Assinatura


@admin.register(Assinatura)
class AssinaturaAdmin(admin.ModelAdmin):
    list_display = ["descricao", "fornecedor", "valor", "periodicidade", "dia_vencimento", "status", "data_inicio"]
    list_filter = ["status", "periodicidade", "fornecedor"]
    search_fields = ["descricao", "fornecedor__nome"]
    date_hierarchy = "data_inicio"
    ordering = ["-data_inicio"]

