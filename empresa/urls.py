from django.urls import path
from . import views

urlpatterns = [
    path("", views.empresa_lista, name="empresa_lista"),
    path("novo/", views.empresa_criar, name="empresa_criar"),
    path("<int:pk>/editar/", views.empresa_editar, name="empresa_editar"),
    path("<int:pk>/excluir/", views.empresa_excluir, name="empresa_excluir"),
]
