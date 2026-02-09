from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Empresa
from .forms import EmpresaForm


@login_required(login_url="login")
def empresa_lista(request):
    empresas = Empresa.objects.all().order_by("nome")

    context = {
        "empresas": empresas,
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
