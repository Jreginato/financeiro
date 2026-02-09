from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import CustomAuthenticationForm


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("contas_pagar_lista")

    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("contas_pagar_lista")
    else:
        form = CustomAuthenticationForm()

    return render(request, "login/login.html", {"form": form})


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")
