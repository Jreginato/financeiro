from django.urls import path
from . import views

urlpatterns = [
    # Contas a Pagar
    path("", views.contas_pagar_lista, name="contas_pagar_lista"),
    path("novo/", views.conta_pagar_criar, name="conta_pagar_criar"),
    path("<int:pk>/editar/", views.conta_pagar_editar, name="conta_pagar_editar"),
    path("<int:pk>/excluir/", views.conta_pagar_excluir, name="conta_pagar_excluir"),
    path("contas-pagar/baixa/", views.baixa_selecao, name="contas_pagar_baixa_selecao"),
    path("contas-pagar/baixa/confirmar/", views.baixa_confirmar, name="contas_pagar_baixa_confirmar"),

    # Plano de Contas
    path("plano/", views.plano_contas_lista, name="plano_contas_lista"),
    path("plano/novo/", views.plano_contas_criar, name="plano_contas_criar"),
    path("plano/<int:pk>/editar/", views.plano_contas_editar, name="plano_contas_editar"),
    path("plano/<int:pk>/excluir/", views.plano_contas_excluir, name="plano_contas_excluir"),

    # Cópia de Contas
    path("copia/", views.copia_selecao, name="contas_pagar_copia_selecao"),
    path("copia/confirmar/", views.copia_confirmar, name="contas_pagar_copia_confirmar"),

    # Recorrência de Contas
    path("<int:pk>/recorrencia/", views.recorrencia_quantidade, name="contas_pagar_recorrencia"),
    path("<int:pk>/recorrencia/previa/", views.recorrencia_previa, name="contas_pagar_recorrencia_previa"),
    path("recorrencia/confirmar/", views.recorrencia_confirmar, name="contas_pagar_recorrencia_confirmar"),
]