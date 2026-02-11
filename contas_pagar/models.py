from django.db import models
from django.utils import timezone
from datetime import timedelta, date
from empresa import models as emp

from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from empresa import models as emp



class PlanoDeContas(models.Model):
    class Tipo(models.TextChoices):
        GRUPO = "grupo", "Grupo"
        CONTA = "conta", "Conta"

    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=255)

    tipo = models.CharField(
        max_length=10,
        choices=Tipo.choices,
        default=Tipo.CONTA
    )

    pai = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='filhos'
    )

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Plano de contas"
        verbose_name_plural = "Plano de contas"



    def __str__(self):
        return f"{self.codigo} - {self.nome}"




class ContaPagar(models.Model):

    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        PAGA = "paga", "Paga"
        ATRASADA = "atrasada", "Atrasada"
        CANCELADA = "cancelada", "Cancelada"

    class Recorrencia(models.TextChoices):
        NENHUMA = "nenhuma", "Sem recorrência"
        SEMANAL = "semanal", "Semanal"
        MENSAL = "mensal", "Mensal"
        ANUAL = "anual", "Anual"
        PERSONALIZADA = "personalizada", "Personalizada"

    descricao = models.CharField(max_length=255)

    fornecedor = models.ForeignKey(
        emp.Empresa,
        on_delete=models.PROTECT,
        related_name="contas_pagar",
        null=True,
        blank=False,
    )

    plano_conta = models.ForeignKey(
        "PlanoDeContas",
        on_delete=models.PROTECT,
        limit_choices_to={"tipo": "conta"},
        related_name="contas_pagar",
    )

    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_emissao = models.DateField(default=timezone.now)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    recorrencia_gerada = models.BooleanField(default=False)
    quantidade_recorrencias = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Quantidade de parcelas futuras a gerar"
    )
    conta_origem = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="parcelas_geradas"
    )

    valor_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )

    recorrencia = models.CharField(
        max_length=20,
        choices=Recorrencia.choices,
        default=Recorrencia.NENHUMA,
    )



    observacoes = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conta a pagar"
        verbose_name_plural = "Contas a pagar"

    