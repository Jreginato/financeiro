from django.db import models
from django.utils import timezone
from empresa import models as emp


class ContaReceber(models.Model):

    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        RECEBIDA = "recebida", "Recebida"
        ATRASADA = "atrasada", "Atrasada"
        CANCELADA = "cancelada", "Cancelada"

    descricao = models.CharField(max_length=255)

    cliente = models.ForeignKey(
        emp.Empresa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contas_receber",
    )

    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_emissao = models.DateField(default=timezone.now)
    data_vencimento = models.DateField()
    data_recebimento = models.DateField(null=True, blank=True)

    valor_recebido = models.DecimalField(
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

    observacoes = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conta a receber"
        verbose_name_plural = "Contas a receber"

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"
