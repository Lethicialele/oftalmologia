from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('cadastrarProcedimentos/', views.cadastrarProcedimentos, name="cadastrarProcedimentos"),
    path('mostrarProcedimentos/', views.mostrarProcedimentos, name="mostrarProcedimentos"),
    path('cadastrarPacientes/', lambda request: redirect('cadastrarPacientes', permanent=True)),
    path('cadastrarMedicos/', lambda request: redirect('cadastrarMedicos', permanent=True)),
    path('cadastrarAgendamentos/', lambda request: redirect('cadastrarAgendamentos', permanent=True)),
    path('cadastrarProcedimentos/', lambda request: redirect('cadastrarProcedimentos', permanent=True)),
    path('consultarAgendaDia/', lambda request: redirect('consultarAgendaDia', permanent=True)),
    path('home', lambda request: redirect('', permanent=True)),
]