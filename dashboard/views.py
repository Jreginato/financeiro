from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, Q
from decimal import Decimal
import calendar
from datetime import timedelta
from contas_pagar.models import ContaPagar
from contas_receber.models import ContaReceber


@login_required(login_url="login")
def dashboard(request):
    hoje = timezone.now().date()
    primeiro_dia = hoje.replace(day=1)
    ultimo_dia = hoje.replace(day=calendar.monthrange(hoje.year, hoje.month)[1])
    proximos_7_dias = hoje + timedelta(days=7)
    
    # =========================================================================
    # CONTAS A PAGAR - Métricas Principais
    # =========================================================================
    
    # Contas vencidas (não pagas e data vencimento < hoje)
    contas_vencidas = ContaPagar.objects.filter(
        status__in=[ContaPagar.Status.PENDENTE, ContaPagar.Status.ATRASADA],
        data_vencimento__lt=hoje
    )
    total_vencidas = contas_vencidas.aggregate(total=Sum('valor'))['total'] or Decimal('0')
    qtd_vencidas = contas_vencidas.count()
    
    # Contas vencendo nos próximos 7 dias
    contas_vencendo = ContaPagar.objects.filter(
        status=ContaPagar.Status.PENDENTE,
        data_vencimento__gte=hoje,
        data_vencimento__lte=proximos_7_dias
    )
    total_vencendo = contas_vencendo.aggregate(total=Sum('valor'))['total'] or Decimal('0')
    qtd_vencendo = contas_vencendo.count()
    
    # Total a pagar no mês (pendentes + atrasadas do mês atual)
    total_pagar_mes = ContaPagar.objects.filter(
        status__in=[ContaPagar.Status.PENDENTE, ContaPagar.Status.ATRASADA],
        data_vencimento__gte=primeiro_dia,
        data_vencimento__lte=ultimo_dia
    ).aggregate(total=Sum('valor'))['total'] or Decimal('0')
    
    # Total pago no mês
    total_pago_mes = ContaPagar.objects.filter(
        status=ContaPagar.Status.PAGA,
        data_pagamento__gte=primeiro_dia,
        data_pagamento__lte=ultimo_dia
    ).aggregate(total=Sum('valor_pago'))['total'] or Decimal('0')
    
    # Total previsto no mês (soma de todas do mês, independente de status)
    total_previsto_mes = ContaPagar.objects.filter(
        data_vencimento__gte=primeiro_dia,
        data_vencimento__lte=ultimo_dia
    ).aggregate(total=Sum('valor'))['total'] or Decimal('0')
    
    # =========================================================================
    # CONTAS A RECEBER - Resumo
    # =========================================================================
    
    # Total a receber no mês
    total_receber_mes = ContaReceber.objects.filter(
        status__in=[ContaReceber.Status.PENDENTE, ContaReceber.Status.ATRASADA],
        data_vencimento__gte=primeiro_dia,
        data_vencimento__lte=ultimo_dia
    ).aggregate(total=Sum('valor'))['total'] or Decimal('0')
    
    # Total recebido no mês
    total_recebido_mes = ContaReceber.objects.filter(
        status=ContaReceber.Status.RECEBIDA,
        data_recebimento__gte=primeiro_dia,
        data_recebimento__lte=ultimo_dia
    ).aggregate(total=Sum('valor_recebido'))['total'] or Decimal('0')
    
    # =========================================================================
    # SALDO PROJETADO
    # =========================================================================
    
    saldo_projetado = total_receber_mes - total_pagar_mes
    
    # =========================================================================
    # GRÁFICO: GASTOS POR CATEGORIA (Top 10)
    # =========================================================================
    
    gastos_por_categoria = ContaPagar.objects.filter(
        data_vencimento__gte=primeiro_dia,
        data_vencimento__lte=ultimo_dia,
        status__in=[ContaPagar.Status.PAGA, ContaPagar.Status.PENDENTE, ContaPagar.Status.ATRASADA]
    ).values(
        'plano_conta__nome'
    ).annotate(
        total=Sum('valor')
    ).order_by('-total')[:10]
    
    categorias_labels = [item['plano_conta__nome'] or 'Sem Categoria' for item in gastos_por_categoria]
    categorias_valores = [float(item['total']) for item in gastos_por_categoria]
    
    # =========================================================================
    # GRÁFICO: EVOLUÇÃO MENSAL (Últimos 6 meses)
    # =========================================================================
    
    meses_data = []
    meses_pago = []
    meses_recebido = []
    
    for i in range(5, -1, -1):  # 6 meses atrás até agora
        mes_ref = hoje.replace(day=1) - timedelta(days=i * 30)
        primeiro = mes_ref.replace(day=1)
        ultimo = mes_ref.replace(day=calendar.monthrange(mes_ref.year, mes_ref.month)[1])
        
        pago = ContaPagar.objects.filter(
            status=ContaPagar.Status.PAGA,
            data_pagamento__gte=primeiro,
            data_pagamento__lte=ultimo
        ).aggregate(total=Sum('valor_pago'))['total'] or Decimal('0')
        
        recebido = ContaReceber.objects.filter(
            status=ContaReceber.Status.RECEBIDA,
            data_recebimento__gte=primeiro,
            data_recebimento__lte=ultimo
        ).aggregate(total=Sum('valor_recebido'))['total'] or Decimal('0')
        
        meses_data.append(f"{mes_ref.strftime('%b/%y')}")
        meses_pago.append(float(pago))
        meses_recebido.append(float(recebido))
    
    # =========================================================================
    # MAIORES DESPESAS DO MÊS (Top 5)
    # =========================================================================
    
    maiores_despesas = ContaPagar.objects.filter(
        data_vencimento__gte=primeiro_dia,
        data_vencimento__lte=ultimo_dia
    ).order_by('-valor')[:5]
    
    # =========================================================================
    # PRÓXIMAS CONTAS A VENCER (5 próximas)
    # =========================================================================
    
    proximas_contas = ContaPagar.objects.filter(
        status__in=[ContaPagar.Status.PENDENTE, ContaPagar.Status.ATRASADA],
        data_vencimento__gte=hoje
    ).order_by('data_vencimento')[:5]
    
    context = {
        # Métricas principais
        'total_vencidas': total_vencidas,
        'qtd_vencidas': qtd_vencidas,
        'total_vencendo': total_vencendo,
        'qtd_vencendo': qtd_vencendo,
        'total_pagar_mes': total_pagar_mes,
        'total_pago_mes': total_pago_mes,
        'total_previsto_mes': total_previsto_mes,
        'total_receber_mes': total_receber_mes,
        'total_recebido_mes': total_recebido_mes,
        'saldo_projetado': saldo_projetado,
        
        # Dados para gráficos
        'categorias_labels': categorias_labels,
        'categorias_valores': categorias_valores,
        'meses_data': meses_data,
        'meses_pago': meses_pago,
        'meses_recebido': meses_recebido,
        
        # Listagens
        'maiores_despesas': maiores_despesas,
        'proximas_contas': proximas_contas,
        
        # Data atual
        'hoje': hoje,
    }
    
    return render(request, 'dashboard/index.html', context)

