from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('cadastrarPacientes/', views.cadastrarPacientes, name="cadastrarPacientes"),
    path('mostrarPacientes/', views.mostrarPacientes, name="mostrarPacientes"),
    path('cadastrarPacientes/', lambda request: redirect('cadastrarPacientes', permanent=True)),
    path('cadastrarMedicos/', lambda request: redirect('cadastrarMedicos', permanent=True)),
    path('cadastrarAgendamentos/', lambda request: redirect('cadastrarAgendamentos', permanent=True)),
    path('cadastrarProcedimentos/', lambda request: redirect('cadastrarProcedimentos', permanent=True)),
    path('consultarAgendaDia/', lambda request: redirect('consultarAgendaDia', permanent=True)),
    path('home', lambda request: redirect('', permanent=True)),
]