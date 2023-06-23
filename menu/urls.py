from django.urls import path
from django.shortcuts import redirect
from menu import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrarPaciente/', lambda request: redirect('cadastrarPaciente', permanent=True)),
    path('cadastrarAgendamento/', lambda request: redirect('cadastrarAgendamento', permanent=True)),
    path('cadastrarProcedimento/', lambda request: redirect('cadastrarProcedimento', permanent=True)),
    path('consultarAgendaDia/', lambda request: redirect('consultarAgendaDia', permanent=True)),
]