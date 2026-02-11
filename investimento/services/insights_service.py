from decimal import Decimal
from django.db.models import Sum, Count, Q
from ..models import Investimento


class InvestimentoInsightsService:
    """Service para calcular insights e métricas estratégicas de investimentos"""

    @staticmethod
    def calcular_insights(empresa=None):
        """
        Calcula todas as métricas e insights dos investimentos
        
        Args:
            empresa: Filtrar por empresa específica (opcional)
        
        Returns:
            dict com todas as métricas calculadas
        """
        # Base query
        qs = Investimento.objects.all()
        if empresa:
            qs = qs.filter(empresa=empresa)

        # Separa compras e vendas
        compras = qs.filter(tipo_operacao=Investimento.TipoOperacao.COMPRA)
        vendas = qs.filter(tipo_operacao=Investimento.TipoOperacao.VENDA)

        # Totais gerais
        total_investido = compras.aggregate(
            total=Sum('valor_total')
        )['total'] or Decimal('0.00')

        total_resgatado = vendas.aggregate(
            total=Sum('valor_total')
        )['total'] or Decimal('0.00')

        # Total em taxas
        total_taxas = qs.aggregate(
            corretagem=Sum('taxa_corretagem'),
            custodia=Sum('taxa_custodia'),
            emolumentos=Sum('emolumentos'),
            impostos=Sum('impostos'),
            outras=Sum('outras_taxas')
        )
        
        total_taxas_geral = (
            (total_taxas['corretagem'] or Decimal('0.00')) +
            (total_taxas['custodia'] or Decimal('0.00')) +
            (total_taxas['emolumentos'] or Decimal('0.00')) +
            (total_taxas['impostos'] or Decimal('0.00')) +
            (total_taxas['outras'] or Decimal('0.00'))
        )

        # Saldo atual (investido - resgatado)
        saldo_atual = total_investido - total_resgatado

        # Lucro/Prejuízo realizado (simplificado - vendas menos compras)
        lucro_prejuizo = total_resgatado - total_investido

        # Distribuição por tipo de ativo
        por_tipo_ativo = []
        for tipo in Investimento.TipoAtivo.choices:
            tipo_codigo = tipo[0]
            tipo_nome = tipo[1]
            
            compras_tipo = compras.filter(tipo_ativo=tipo_codigo).aggregate(
                total=Sum('valor_total'),
                qtd=Count('id')
            )
            vendas_tipo = vendas.filter(tipo_ativo=tipo_codigo).aggregate(
                total=Sum('valor_total'),
                qtd=Count('id')
            )
            
            total_compras = compras_tipo['total'] or Decimal('0.00')
            total_vendas = vendas_tipo['total'] or Decimal('0.00')
            saldo = total_compras - total_vendas
            
            if total_compras > 0 or total_vendas > 0:
                por_tipo_ativo.append({
                    'tipo': tipo_nome,
                    'tipo_codigo': tipo_codigo,
                    'total_compras': total_compras,
                    'total_vendas': total_vendas,
                    'saldo': saldo,
                    'qtd_operacoes': (compras_tipo['qtd'] or 0) + (vendas_tipo['qtd'] or 0)
                })

        # Ordena por saldo
        por_tipo_ativo.sort(key=lambda x: x['saldo'], reverse=True)

        # Posição consolidada por ticker (todas operações de compra e venda)
        # Agrupa por ticker
        tickers_consolidado = {}
        for inv in qs:
            ticker = inv.ticker
            if ticker not in tickers_consolidado:
                tickers_consolidado[ticker] = {
                    'ticker': ticker,
                    'nome': inv.nome_ativo or ticker,
                    'tipo_ativo': inv.get_tipo_ativo_display(),
                    'quantidade_total': Decimal('0'),
                    'valor_total_investido': Decimal('0'),
                    'compras': [],
                    'vendas': []
                }
            
            if inv.tipo_operacao == Investimento.TipoOperacao.COMPRA:
                tickers_consolidado[ticker]['quantidade_total'] += inv.quantidade
                tickers_consolidado[ticker]['valor_total_investido'] += inv.valor_total
                tickers_consolidado[ticker]['compras'].append(inv)
            else:
                tickers_consolidado[ticker]['quantidade_total'] -= inv.quantidade
                tickers_consolidado[ticker]['valor_total_investido'] -= inv.valor_total
                tickers_consolidado[ticker]['vendas'].append(inv)

        # Calcula preço médio
        posicao_consolidada = []
        for ticker_data in tickers_consolidado.values():
            if ticker_data['quantidade_total'] > 0:
                preco_medio = ticker_data['valor_total_investido'] / ticker_data['quantidade_total']
                posicao_consolidada.append({
                    'ticker': ticker_data['ticker'],
                    'nome': ticker_data['nome'],
                    'tipo_ativo': ticker_data['tipo_ativo'],
                    'quantidade': ticker_data['quantidade_total'],
                    'preco_medio': preco_medio,
                    'valor_investido': ticker_data['valor_total_investido']
                })

        # Ordena por valor investido
        posicao_consolidada.sort(key=lambda x: x['valor_investido'], reverse=True)

        # Estatísticas gerais
        total_operacoes = qs.count()
        total_compras = compras.count()
        total_vendas = vendas.count()

        return {
            'resumo': {
                'total_investido': total_investido,
                'total_resgatado': total_resgatado,
                'saldo_atual': saldo_atual,
                'lucro_prejuizo': lucro_prejuizo,
                'total_taxas': total_taxas_geral,
                'total_operacoes': total_operacoes,
                'total_compras': total_compras,
                'total_vendas': total_vendas,
            },
            'por_tipo_ativo': por_tipo_ativo,
            'posicao_consolidada': posicao_consolidada,
            'detalhes_taxas': total_taxas,
        }