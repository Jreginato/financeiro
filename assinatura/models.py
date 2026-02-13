from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from empresa import models as emp


class Assinatura(models.Model):

    class Status(models.TextChoices):
        ATIVA = "ativa", "Ativa"
        SUSPENSA = "suspensa", "Suspensa"
        CANCELADA = "cancelada", "Cancelada"

    class Periodicidade(models.TextChoices):
        MENSAL = "mensal", "Mensal"
        BIMESTRAL = "bimestral", "Bimestral"
        TRIMESTRAL = "trimestral", "Trimestral"
        SEMESTRAL = "semestral", "Semestral"
        ANUAL = "anual", "Anual"

    descricao = models.CharField(
        max_length=255,
        verbose_name="Descrição"
    )

    fornecedor = models.ForeignKey(
        emp.Empresa,
        on_delete=models.PROTECT,
        related_name="assinaturas",
        verbose_name="Fornecedor"
    )

    plano_conta = models.ForeignKey(
        "contas_pagar.PlanoDeContas",
        on_delete=models.PROTECT,
        limit_choices_to={"tipo": "conta"},
        related_name="assinaturas",
        verbose_name="Plano de Contas"
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor"
    )

    periodicidade = models.CharField(
        max_length=20,
        choices=Periodicidade.choices,
        default=Periodicidade.MENSAL,
        verbose_name="Periodicidade"
    )

    dia_vencimento = models.PositiveIntegerField(
        verbose_name="Dia do Vencimento",
        help_text="Dia do mês em que a assinatura vence (1-28)"
    )

    data_inicio = models.DateField(
        default=timezone.now,
        verbose_name="Data de Início"
    )

    data_cancelamento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Cancelamento"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ATIVA,
        verbose_name="Status"
    )

    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações"
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Assinatura"
        verbose_name_plural = "Assinaturas"
        ordering = ["-data_inicio"]

    def __str__(self):
        return f"{self.descricao} - {self.fornecedor} (R$ {self.valor})"

    def clean(self):
        """Validações customizadas"""
        if self.dia_vencimento < 1 or self.dia_vencimento > 28:
            raise ValidationError({
                'dia_vencimento': 'Dia de vencimento deve estar entre 1 e 28.'
            })

        if self.data_cancelamento and self.data_cancelamento < self.data_inicio:
            raise ValidationError({
                'data_cancelamento': 'Data de cancelamento não pode ser anterior à data de início.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)




