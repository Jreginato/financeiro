from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import calendar
from .models import ContaReceber
from .forms import ContaReceberForm
from .services.recebimento_service import RecebimentoService


@login_required(login_url="login")
def contas_receber_lista(request):
    hoje = timezone.now().date()
    primeiro_dia = hoje.replace(day=1)
    ultimo_dia = hoje.replace(day=calendar.monthrange(hoje.year, hoje.month)[1])

    # Detecta se NÃO há filtros na URL
    nenhum_parametro = len(request.GET) == 0

    # Normaliza GET
    status = request.GET.get("status") or "padrao"
    data_inicio = request.GET.get("inicio") or None
    data_fim = request.GET.get("fim") or None

    # -----------------------------
    # 1) ENTRADA NA TELA (PADRÃO)
    # -----------------------------
    if nenhum_parametro or status == "padrao":
        status = "padrao"
        data_inicio = primeiro_dia
        data_fim = ultimo_dia

    # -----------------------------
    # 2) FILTRO ESPECIAL: TODOS
    # -----------------------------
    if status == "todos":
        # Sem filtro de datas, mostra tudo
        contas = ContaReceber.objects.all()
    else:
        # 2) GARANTIA: datas nunca podem ser None
        if not data_inicio:
            data_inicio = primeiro_dia
        if not data_fim:
            data_fim = ultimo_dia

        # 3) FILTRO DE DATAS (sempre obrigatório)
        contas = ContaReceber.objects.filter(
            data_vencimento__gte=data_inicio,
            data_vencimento__lte=data_fim
        )

    # 4) FILTRO DE STATUS
    if status == "padrao":
        contas = contas.filter(
            status__in=[
                ContaReceber.Status.PENDENTE,
                ContaReceber.Status.ATRASADA
            ]
        )
    elif status not in ["todos", "padrao"] and status:
        contas = contas.filter(status=status)

    contas = contas.order_by("data_vencimento")

    # Paginação
    paginator = Paginator(contas, 20)  # 20 itens por página
    page = request.GET.get('page', 1)
    
    try:
        contas_paginadas = paginator.page(page)
    except PageNotAnInteger:
        contas_paginadas = paginator.page(1)
    except EmptyPage:
        contas_paginadas = paginator.page(paginator.num_pages)

    context = {
        "contas": contas_paginadas,
        "page_obj": contas_paginadas,
        "is_paginated": paginator.num_pages > 1,
        "status": "" if status == "padrao" else status,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return render(request, "contas_receber/lista.html", context)


@login_required(login_url="login")
def conta_receber_criar(request):
    if request.method == "POST":
        form = ContaReceberForm(request.POST)
        if form.is_valid():
            conta = form.save()
            return redirect("contas_receber_lista")
    else:
        form = ContaReceberForm()

    return render(request, "contas_receber/form.html", {"form": form, "modo": "criar"})


@login_required(login_url="login")
def conta_receber_editar(request, pk):
    conta = get_object_or_404(ContaReceber, pk=pk)

    if request.method == "POST":
        form = ContaReceberForm(request.POST, instance=conta)
        if form.is_valid():
            conta = form.save()
            return redirect("contas_receber_lista")
    else:
        form = ContaReceberForm(instance=conta)

    return render(request, "contas_receber/form.html", {"form": form, "modo": "editar", "conta": conta})


@login_required(login_url="login")
def conta_receber_excluir(request, pk):
    conta = get_object_or_404(ContaReceber, pk=pk)

    if request.method == "POST":
        conta.delete()
        return redirect("contas_receber_lista")

    return render(request, "contas_receber/confirmar_exclusao.html", {
        "conta": conta
    })

@login_required(login_url="login")
def recebimento_selecao(request):
    if request.method != "POST":
        return redirect("contas_receber_lista")

    ids = request.POST.getlist("contas")

    if not ids:
        return redirect("contas_receber_lista")

    contas = ContaReceber.objects.filter(id__in=ids)

    hoje = timezone.now().date()

    return render(request, "contas_receber/recebimento_tabela.html", {
        "contas": contas,
        "hoje": hoje,
    })


@login_required(login_url="login")
def recebimento_confirmar(request):
    if request.method != "POST":
        return redirect("contas_receber_lista")

    ids = request.POST.getlist("contas")
    contas = ContaReceber.objects.filter(id__in=ids)

    RecebimentoService.receber_em_lote(contas, request.POST)

    return redirect("contas_receber_lista")
