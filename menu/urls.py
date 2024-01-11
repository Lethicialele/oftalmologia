from django.urls import path
from django.shortcuts import redirect
from menu import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('cadastrarPacientes/', lambda request: redirect('cadastrarPacientes', permanent=True)),
    path('cadastrarMedicos/', lambda request: redirect('cadastrarMedicos', permanent=True)),
    path('cadastrarAgendamentos/', lambda request: redirect('cadastrarAgendamentos', permanent=True)),
    path('cadastrarProcedimentos/', lambda request: redirect('cadastrarProcedimentos', permanent=True)),
    path('consultarAgendaDia/', lambda request: redirect('consultarAgendaDia', permanent=True)),
    path('gerarAgenda/', lambda request: redirect('gerarAgenda', permanent=True)),
    path('consultarFilaEsperaPacientes/', lambda request: redirect('consultarFilaEsperaPacientes', permanent=True)),
]