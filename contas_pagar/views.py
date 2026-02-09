from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import calendar
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

    hoje = timezone.now().date()

    return render(request, "contas_pagar/copia_tabela.html", {
        "contas": contas,
        "hoje": hoje,
    })


@login_required(login_url="login")
def copia_confirmar(request):
    if request.method != "POST":
        return redirect("contas_pagar_lista")

    ids = request.POST.getlist("contas")
    contas = ContaPagar.objects.filter(id__in=ids)

    PagamentoService.copiar_em_lote(contas, request.POST)

    return redirect("contas_pagar_lista")