from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Empresa
from .forms import EmpresaForm


@login_required(login_url="login")
def empresa_lista(request):
    empresas = Empresa.objects.all().order_by("nome")

    # Paginação
    paginator = Paginator(empresas, 20)  # 20 itens por página
    page = request.GET.get('page', 1)
    
    try:
        empresas_paginadas = paginator.page(page)
    except PageNotAnInteger:
        empresas_paginadas = paginator.page(1)
    except EmptyPage:
        empresas_paginadas = paginator.page(paginator.num_pages)

    context = {
        "empresas": empresas_paginadas,
        "page_obj": empresas_paginadas,
        "is_paginated": paginator.num_pages > 1,
    }

    return render(request, "empresa/lista.html", context)


@login_required(login_url="login")
def empresa_criar(request):
    if request.method == "POST":
        form = EmpresaForm(request.POST)
        if form.is_valid():
            empresa = form.save()
            return redirect("empresa_lista")
    else:
        form = EmpresaForm()

    return render(request, "empresa/form.html", {"form": form, "modo": "criar"})


@login_required(login_url="login")
def empresa_editar(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)

    if request.method == "POST":
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            empresa = form.save()
            return redirect("empresa_lista")
    else:
        form = EmpresaForm(instance=empresa)

    return render(request, "empresa/form.html", {"form": form, "modo": "editar", "empresa": empresa})


@login_required(login_url="login")
def empresa_excluir(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)

    if request.method == "POST":
        empresa.delete()
        return redirect("empresa_lista")

    return render(request, "empresa/confirmar_exclusao.html", {
        "empresa": empresa
    })
