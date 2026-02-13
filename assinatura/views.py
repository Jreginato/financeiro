from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Assinatura
from .forms import AssinaturaForm


@login_required(login_url="login")
def assinatura_lista(request):
    status = request.GET.get("status", "")

    assinaturas = Assinatura.objects.all()

    if status:
        assinaturas = assinaturas.filter(status=status)

    assinaturas = assinaturas.order_by("-data_inicio")

    # Paginação
    paginator = Paginator(assinaturas, 20)
    page = request.GET.get('page', 1)
    
    try:
        assinaturas_paginadas = paginator.page(page)
    except PageNotAnInteger:
        assinaturas_paginadas = paginator.page(1)
    except EmptyPage:
        assinaturas_paginadas = paginator.page(paginator.num_pages)

    context = {
        "assinaturas": assinaturas_paginadas,
        "page_obj": assinaturas_paginadas,
        "is_paginated": paginator.num_pages > 1,
        "status": status,
    }

    return render(request, "assinatura/lista.html", context)


@login_required(login_url="login")
def assinatura_criar(request):
    if request.method == "POST":
        form = AssinaturaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("assinatura_lista")
    else:
        form = AssinaturaForm()

    return render(request, "assinatura/form.html", {"form": form, "titulo": "Nova Assinatura"})


@login_required(login_url="login")
def assinatura_editar(request, pk):
    assinatura = get_object_or_404(Assinatura, pk=pk)

    if request.method == "POST":
        form = AssinaturaForm(request.POST, instance=assinatura)
        if form.is_valid():
            form.save()
            return redirect("assinatura_lista")
    else:
        form = AssinaturaForm(instance=assinatura)

    return render(request, "assinatura/form.html", {"form": form, "titulo": "Editar Assinatura"})


@login_required(login_url="login")
def assinatura_excluir(request, pk):
    assinatura = get_object_or_404(Assinatura, pk=pk)

    if request.method == "POST":
        assinatura.delete()
        return redirect("assinatura_lista")

    return render(request, "assinatura/confirmar_exclusao.html", {"assinatura": assinatura})

