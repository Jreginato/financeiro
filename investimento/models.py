from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from empresa.models import Empresa


class Investimento(models.Model):
    """
    Modelo para registrar investimentos em diversos tipos de ativos.
    Permite controle de compras e vendas de ações, criptomoedas, FIIs, renda fixa, etc.
    """
    
    class TipoAtivo(models.TextChoices):
        ACOES = 'acoes', 'Ações'
        CRIPTOMOEDA = 'criptomoeda', 'Criptomoeda'
        FII = 'fii', 'Fundo Imobiliário'
        RENDA_FIXA = 'renda_fixa', 'Renda Fixa'
        CDB = 'cdb', 'CDB'
        LCI = 'lci', 'LCI'
        LCA = 'lca', 'LCA'
        TESOURO_DIRETO = 'tesouro_direto', 'Tesouro Direto'
        DEBENTURES = 'debentures', 'Debêntures'
        ETF = 'etf', 'ETF'
        OUTROS = 'outros', 'Outros'
    
    class TipoOperacao(models.TextChoices):
        COMPRA = 'compra', 'Compra'
        VENDA = 'venda', 'Venda'
    
    # Identificação do ativo
    tipo_ativo = models.CharField(
        max_length=20,
        choices=TipoAtivo.choices,
        verbose_name='Tipo de Ativo'
    )
    
    ticker = models.CharField(
        max_length=20,
        verbose_name='Ticker/Código',
        help_text='Ex: PETR4, BTCUSD, MXRF11, etc.'
    )
    
    nome_ativo = models.CharField(
        max_length=200,
        verbose_name='Nome do Ativo',
        blank=True,
        help_text='Ex: Petrobras PN, Bitcoin, Maxi Renda FII'
    )
    
    # Dados da operação
    tipo_operacao = models.CharField(
        max_length=10,
        choices=TipoOperacao.choices,
        default=TipoOperacao.COMPRA,
        verbose_name='Tipo de Operação'
    )
    
    data_operacao = models.DateField(
        verbose_name='Data da Operação'
    )
    
    quantidade = models.DecimalField(
        max_digits=18,
        decimal_places=8,
        validators=[MinValueValidator(Decimal('0.00000001'))],
        verbose_name='Quantidade',
        help_text='Quantidade de ativos comprados/vendidos'
    )
    
    preco_unitario = models.DecimalField(
        max_digits=18,
        decimal_places=8,
        validators=[MinValueValidator(Decimal('0.00000001'))],
        verbose_name='Preço Unitário',
        help_text='Preço por unidade do ativo'
    )
    
    valor_total = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor Total',
        help_text='Valor total da operação (quantidade × preço unitário)'
    )
    
    # Custos operacionais
    taxa_corretagem = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Taxa de Corretagem'
    )
    
    taxa_custodia = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Taxa de Custódia'
    )
    
    emolumentos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Emolumentos',
        help_text='Taxas da B3'
    )
    
    impostos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Impostos',
        help_text='IR, IOF, etc.'
    )
    
    outras_taxas = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Outras Taxas'
    )
    
    # Informações adicionais
    data_vencimento = models.DateField(
        verbose_name='Data de Vencimento',
        blank=True,
        null=True,
        help_text='Para ativos de renda fixa'
    )
    
    rentabilidade_contratada = models.CharField(
        max_length=100,
        verbose_name='Rentabilidade Contratada',
        blank=True,
        help_text='Ex: 100% CDI, IPCA + 6%, 12% a.a.'
    )
    
    observacoes = models.TextField(
        verbose_name='Observações',
        blank=True
    )
    
    # Relações
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        related_name='investimentos',
        verbose_name='Empresa'
    )
    
    # Auditoria
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        verbose_name = 'Investimento'
        verbose_name_plural = 'Investimentos'
        ordering = ['-data_operacao', '-criado_em']
        indexes = [
            models.Index(fields=['-data_operacao']),
            models.Index(fields=['ticker']),
            models.Index(fields=['tipo_ativo']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_operacao_display()} - {self.ticker} - {self.quantidade} un. - {self.data_operacao.strftime('%d/%m/%Y')}"
