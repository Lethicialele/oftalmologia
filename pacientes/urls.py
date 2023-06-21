from django.urls import path
from . import views

urlpatterns = [
    path('cadastrarPacientes/', views.cadastrarPacientes, name="cadastrarPacientes"),
    path('verPacientes/', views.verPacientes, name="verPacientes")
]