from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('cadastrarMedicos/', views.cadastrarMedicos, name="cadastrarMedicos"),
    path('cadastrarPacientes/', lambda request: redirect('cadastrarPacientes', permanent=True)),
    path('cadastrarMedicos/', lambda request: redirect('cadastrarMedicos', permanent=True)),
    path('loginMedicos/', views.loginMedicos, name='loginMedicos'),
    path('cadastrarAgendamentos/', lambda request: redirect('cadastrarAgendamentos', permanent=True)),
    path('cadastrarProcedimentos/', lambda request: redirect('cadastrarProcedimentos', permanent=True)),
    path('consultarAgendaDia/', lambda request: redirect('consultarAgendaDia', permanent=True)),
    path('home', lambda request: redirect('', permanent=True)),
    path('atualizarCadastrorMedicos/', views.atualizarCadastrorMedicos, name="atualizarCadastrorMedicos"),
]