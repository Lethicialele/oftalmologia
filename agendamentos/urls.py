from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('cadastrarAgendamentos/', views.cadastrarAgendamentos, name="cadastrarAgendamentos"),
    path('consultarAgendaDia/', views.consultarAgendaDia, name="consultarAgendaDia"),
    path('imprimirAgenda/<str:data_selecionada>/', views.imprimirAgenda, name='imprimirAgenda'),
    path('confirmarAgendamentos/', views.confirmarAgendamentos, name='confirmarAgendamentos'),
    path('cadastrarPacientes/', lambda request: redirect('cadastrarPacientes', permanent=True)),
    path('cadastrarMedicos/', lambda request: redirect('cadastrarMedicos', permanent=True)),
    path('cadastrarAgendamentos/', lambda request: redirect('cadastrarAgendamentos', permanent=True)),
    path('cadastrarProcedimentos/', lambda request: redirect('cadastrarProcedimentos', permanent=True)),
    path('consultarAgendaDia/', lambda request: redirect('consultarAgendaDia', permanent=True)),
    path('home', lambda request: redirect('', permanent=True)),

]