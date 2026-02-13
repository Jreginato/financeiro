from django.urls import path
from . import views

urlpatterns = [
    path("", views.assinatura_lista, name="assinatura_lista"),
    path("novo/", views.assinatura_criar, name="assinatura_criar"),
    path("<int:pk>/editar/", views.assinatura_editar, name="assinatura_editar"),
    path("<int:pk>/excluir/", views.assinatura_excluir, name="assinatura_excluir"),
]
