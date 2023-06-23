from django.urls import path
from . import views

urlpatterns = [
    path('cadastrarPacientes/', views.cadastrarPacientes, name="cadastrarPacientes"),
    path('mostrarPacientes/', views.mostrarPacientes, name="mostrarPacientes")
]