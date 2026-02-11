from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import calendar
from datetime import date
from .services.pagamento_service import PagamentoService
from .models import ContaPagar, PlanoDeContas
from .forms import ContaPagarForm, PlanoDeContasForm


@login_required(login_url="login")
def contas_pagar_lista(request):
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
        contas = ContaPagar.objects.all()
    else:
        # 2) GARANTIA: datas nunca podem ser None
        if not data_inicio:
            data_inicio = primeiro_dia
        if not data_fim:
            data_fim = ultimo_dia

        # 3) FILTRO DE DATAS (sempre obrigatório)
        contas = ContaPagar.objects.filter(
            data_vencimento__gte=data_inicio,
            data_vencimento__lte=data_fim
        )

    # 4) FILTRO DE STATUS
    if status == "padrao":
        contas = contas.filter(
            status__in=[
                ContaPagar.Status.PENDENTE,
                ContaPagar.Status.ATRASADA
            ]
        )
    elif status not in ["todos", "padrao"] and status:
        contas = contas.filter(status=status)

    contas = contas.order_by("data_vencimento")

    context = {
        "contas": contas,
        "status": "" if status == "padrao" else status,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return render(request, "contas_pagar/lista.html", context)


@login_required(login_url="login")
def conta_pagar_criar(request):
    if request.method == "POST":
        form = ContaPagarForm(request.POST)
        if form.is_valid():
            conta = form.save()

            if conta.recorrencia != ContaPagar.Recorrencia.NENHUMA and conta.quantidade_recorrencias:
                return redirect("contas_pagar_recorrencia_previa", conta_id=conta.id)

            return redirect("contas_pagar_lista")
    else:
        form = ContaPagarForm()

    return render(request, "contas_pagar/form.html", {"form": form, "modo": "criar"})


@login_required(login_url="login")
def conta_pagar_editar(request, pk):
    conta = get_object_or_404(ContaPagar, pk=pk)

    if request.method == "POST":
        form = ContaPagarForm(request.POST, instance=conta)
        if form.is_valid():
            conta = form.save()

            if conta.recorrencia != ContaPagar.Recorrencia.NENHUMA and conta.quantidade_recorrencias:
                return redirect("contas_pagar_recorrencia_previa", conta_id=conta.id)

            return redirect("contas_pagar_lista")
    else:
        form = ContaPagarForm(instance=conta)

    return render(request, "contas_pagar/form.html", {"form": form, "modo": "editar", "conta": conta})


@login_required(login_url="login")
def conta_pagar_excluir(request, pk):
    conta = get_object_or_404(ContaPagar, pk=pk)

    if request.method == "POST":
        conta.delete()
        return redirect("contas_pagar_lista")

    return render(request, "contas_pagar/confirmar_exclusao.html", {
        "conta": conta
    })

@login_required(login_url="login")
def baixa_selecao(request):
    if request.method != "POST":
        return redirect("contas_pagar_lista")

    ids = request.POST.getlist("contas")

    if not ids:
        return redirect("contas_pagar_lista")

    contas = ContaPagar.objects.filter(id__in=ids)

    hoje = timezone.now().date()

    return render(request, "contas_pagar/baixa_tabela.html", {
        "contas": contas,
        "hoje": hoje,
    })


@login_required(login_url="login")
def baixa_confirmar(request):
    if request.method != "POST":
        return redirect("contas_pagar_lista")

    ids = request.POST.getlist("contas")
    contas = ContaPagar.objects.filter(id__in=ids)

    PagamentoService.baixar_em_lote(contas, request.POST)

    return redirect("contas_pagar_lista")


# ===================================
# PLANO DE CONTAS CRUD
# ===================================

@login_required(login_url="login")
def plano_contas_lista(request):
    planos = PlanoDeContas.objects.all().order_by("codigo")

    context = {
        "planos": planos,
    }

    return render(request, "contas_pagar/plano_contas_lista.html", context)


@login_required(login_url="login")
def plano_contas_criar(request):
    if request.method == "POST":
        form = PlanoDeContasForm(request.POST)
        if form.is_valid():
            plano = form.save()
            return redirect("plano_contas_lista")
    else:
        form = PlanoDeContasForm()

    return render(request, "contas_pagar/plano_contas_form.html", {"form": form, "modo": "criar"})


@login_required(login_url="login")
def plano_contas_editar(request, pk):
    plano = get_object_or_404(PlanoDeContas, pk=pk)

    if request.method == "POST":
        form = PlanoDeContasForm(request.POST, instance=plano)
        if form.is_valid():
            plano = form.save()
            return redirect("plano_contas_lista")
    else:
        form = PlanoDeContasForm(instance=plano)

    return render(request, "contas_pagar/plano_contas_form.html", {"form": form, "modo": "editar", "plano": plano})


@login_required(login_url="login")
def plano_contas_excluir(request, pk):
    plano = get_object_or_404(PlanoDeContas, pk=pk)

    if request.method == "POST":
        plano.delete()
        return redirect("plano_contas_lista")

    return render(request, "contas_pagar/plano_contas_confirmar_exclusao.html", {
        "plano": plano
    })


# ===================================
# CÓPIA DE CONTAS
# ===================================

@login_required(login_url="login")
def copia_selecao(request):
    if request.method != "POST":
        return redirect("contas_pagar_lista")

    ids = request.POST.getlist("contas")

    if not ids:
        return redirect("contas_pagar_lista")

    contas = ContaPagar.objects.filter(id__in=ids)

    # Calcula data de vencimento + 1 mês para cada conta
    contas_com_datas = []
    for conta in contas:
        # Adiciona 1 mês mantendo o dia (ajusta para último dia se necessário)
        ano = conta.data_vencimento.year
        mes = conta.data_vencimento.month + 1
        dia = conta.data_vencimento.day
        
        if mes > 12:
            mes = 1
            ano += 1
        
        # Ajusta o dia se o mês de destino tiver menos dias
        from calendar import monthrange
        ultimo_dia = monthrange(ano, mes)[1]
        if dia > ultimo_dia:
            dia = ultimo_dia
        
        nova_data = date(ano, mes, dia)
        
        contas_com_datas.append({
            'conta': conta,
            'nova_data_vencimento': nova_data
        })

    return render(request, "contas_pagar/copia_tabela.html", {
        "contas_com_datas": contas_com_datas,
    })


@login_required(login_url="login")
def copia_confirmar(request):
    if request.method != "POST":
        return redirect("contas_pagar_lista")

    ids = request.POST.getlist("contas")
    contas = ContaPagar.objects.filter(id__in=ids)

    PagamentoService.copiar_em_lote(contas, request.POST)

    return redirect("contas_pagar_lista")


# ===================================
# RECORRÊNCIA DE CONTAS
# ===================================

@login_required(login_url="login")
def recorrencia_quantidade(request, pk):
    """Solicita a quantidade de lançamentos recorrentes."""
    conta = get_object_or_404(ContaPagar, pk=pk)
    
    if request.method == "POST":
        quantidade = request.POST.get("quantidade")
        if quantidade and int(quantidade) > 0:
            from django.urls import reverse
            url = reverse("contas_pagar_recorrencia_previa", kwargs={"pk": pk})
            return redirect(f"{url}?quantidade={quantidade}")
    
    return render(request, "contas_pagar/recorrencia_quantidade.html", {
        "conta": conta,
    })


@login_required(login_url="login")
def recorrencia_previa(request, pk):
    """Mostra prévia dos lançamentos recorrentes."""
    conta = get_object_or_404(ContaPagar, pk=pk)
    quantidade = int(request.GET.get("quantidade", 1))
    
    if quantidade <= 0 or quantidade > 120:  # Limita a 120 lançamentos
        return redirect("contas_pagar_recorrencia", pk=pk)
    
    # Gera lista de lançamentos futuros
    from calendar import monthrange
    lancamentos = []
    
    for i in range(1, quantidade + 1):
        # Calcula data: adiciona i meses
        ano = conta.data_vencimento.year
        mes = conta.data_vencimento.month + i
        dia = conta.data_vencimento.day
        
        # Ajusta ano se necessário
        while mes > 12:
            mes -= 12
            ano += 1
        
        # Ajusta dia se o mês não tiver esse dia
        ultimo_dia = monthrange(ano, mes)[1]
        if dia > ultimo_dia:
            dia = ultimo_dia
        
        nova_data = date(ano, mes, dia)
        
        lancamentos.append({
            'numero': i,
            'data_vencimento': nova_data,
            'valor': conta.valor,
            'descricao': conta.descricao,
        })
    
    return render(request, "contas_pagar/recorrencia_previa.html", {
        "conta": conta,
        "lancamentos": lancamentos,
        "quantidade": quantidade,
    })


@login_required(login_url="login")
def recorrencia_confirmar(request):
    """Confirma e cria os lançamentos recorrentes."""
    if request.method != "POST":
        return redirect("contas_pagar_lista")
    
    conta_id = request.POST.get("conta_id")
    quantidade = int(request.POST.get("quantidade", 0))
    
    if not conta_id or quantidade <= 0:
        return redirect("contas_pagar_lista")
    
    conta_original = get_object_or_404(ContaPagar, pk=conta_id)
    
    # Cria os lançamentos
    from calendar import monthrange
    for i in range(1, quantidade + 1):
        descricao = request.POST.get(f"descricao_{i}")
        valor = request.POST.get(f"valor_{i}")
        data = request.POST.get(f"data_vencimento_{i}")
        
        if not descricao or not valor or not data:
            continue
        
        # Converte valor
        valor_convertido = float(str(valor).replace(".", "").replace(",", "."))
        if valor_convertido <= 0:
            continue
        
        # Converte data do formato brasileiro (dd/mm/yyyy)
        from datetime import datetime
        data_convertida = datetime.strptime(data, "%d/%m/%Y").date()
        
        # Cria novo lançamento
        ContaPagar.objects.create(
            descricao=descricao,
            fornecedor=conta_original.fornecedor,
            plano_conta=conta_original.plano_conta,
            valor=valor_convertido,
            data_emissao=timezone.now().date(),
            data_vencimento=data_convertida,
            status=ContaPagar.Status.PENDENTE,
            recorrencia=ContaPagar.Recorrencia.NENHUMA,
        )
    
    return redirect("contas_pagar_lista")