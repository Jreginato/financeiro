from django.urls import path
from . import views

urlpatterns = [
    path("", views.investimento_lista, name="investimento_lista"),
    path("insights/", views.investimento_insights, name="investimento_insights"),
    path("novo/", views.investimento_criar, name="investimento_criar"),
    path("<int:pk>/editar/", views.investimento_editar, name="investimento_editar"),
    path("<int:pk>/excluir/", views.investimento_excluir, name="investimento_excluir"),
]
