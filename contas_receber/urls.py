from django.urls import path
from . import views

urlpatterns = [
    path("", views.contas_receber_lista, name="contas_receber_lista"),
    path("novo/", views.conta_receber_criar, name="conta_receber_criar"),
    path("<int:pk>/editar/", views.conta_receber_editar, name="conta_receber_editar"),
    path("<int:pk>/excluir/", views.conta_receber_excluir, name="conta_receber_excluir"),
    path("contas-receber/recebimento/", views.recebimento_selecao, name="contas_receber_recebimento_selecao"),
    path("contas-receber/recebimento/confirmar/", views.recebimento_confirmar, name="contas_receber_recebimento_confirmar"),
]
