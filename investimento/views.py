from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
import calendar
from .models import Investimento
from .forms import InvestimentoForm
from .services.insights_service import InvestimentoInsightsService


@login_required(login_url="login")
def investimento_lista(request):
    hoje = timezone.now().date()
    primeiro_dia = hoje.replace(day=1)
    ultimo_dia = hoje.replace(day=calendar.monthrange(hoje.year, hoje.month)[1])

    # Detecta se NÃO há filtros na URL
    nenhum_parametro = len(request.GET) == 0

    # Normaliza GET
    tipo_ativo = request.GET.get("tipo_ativo") or ""
    tipo_operacao = request.GET.get("tipo_operacao") or ""
    data_inicio = request.GET.get("inicio") or None
    data_fim = request.GET.get("fim") or None

    # Filtro padrão
    if nenhum_parametro:
        data_inicio = primeiro_dia
        data_fim = ultimo_dia

    # Inicia query
    investimentos = Investimento.objects.all()

    # Filtro de datas
    if data_inicio:
        investimentos = investimentos.filter(data_operacao__gte=data_inicio)
    if data_fim:
        investimentos = investimentos.filter(data_operacao__lte=data_fim)

    # Filtro de tipo de ativo
    if tipo_ativo:
        investimentos = investimentos.filter(tipo_ativo=tipo_ativo)

    # Filtro de tipo de operação
    if tipo_operacao:
        investimentos = investimentos.filter(tipo_operacao=tipo_operacao)

    investimentos = investimentos.order_by('-data_operacao', '-criado_em')

    # Paginação
    paginator = Paginator(investimentos, 20)  # 20 itens por página
    page = request.GET.get('page', 1)
    
    try:
        investimentos_paginados = paginator.page(page)
    except PageNotAnInteger:
        investimentos_paginados = paginator.page(1)
    except EmptyPage:
        investimentos_paginados = paginator.page(paginator.num_pages)

    context = {
        "investimentos": investimentos_paginados,
        "page_obj": investimentos_paginados,
        "is_paginated": paginator.num_pages > 1,
        "tipo_ativo": tipo_ativo,
        "tipo_operacao": tipo_operacao,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return render(request, "investimento/lista.html", context)


@login_required(login_url="login")
def investimento_criar(request):
    if request.method == "POST":
        form = InvestimentoForm(request.POST)
        if form.is_valid():
            investimento = form.save()
            return redirect("investimento_lista")
    else:
        form = InvestimentoForm()

    return render(request, "investimento/form.html", {"form": form, "modo": "criar"})


@login_required(login_url="login")
def investimento_editar(request, pk):
    investimento = get_object_or_404(Investimento, pk=pk)

    if request.method == "POST":
        form = InvestimentoForm(request.POST, instance=investimento)
        if form.is_valid():
            investimento = form.save()
            return redirect("investimento_lista")
    else:
        form = InvestimentoForm(instance=investimento)

    return render(request, "investimento/form.html", {
        "form": form,
        "modo": "editar",
        "investimento": investimento
    })


@login_required(login_url="login")
def investimento_excluir(request, pk):
    investimento = get_object_or_404(Investimento, pk=pk)

    if request.method == "POST":
        investimento.delete()
        return redirect("investimento_lista")

    return render(request, "investimento/confirmar_exclusao.html", {
        "investimento": investimento
    })


@login_required(login_url="login")
def investimento_insights(request):
    """Exibe insights e análises estratégicas dos investimentos"""
    insights = InvestimentoInsightsService.calcular_insights()
    
    return render(request, "investimento/insights.html", {
        "insights": insights
    })
