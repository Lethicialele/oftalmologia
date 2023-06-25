from django.urls import path
from . import views

urlpatterns = [
    path('cadastrarAgendamentos/', views.cadastrarAgendamentos, name="cadastrarAgendamentos"),
    path('consultarAgendaDia/', views.consultarAgendaDia, name="consultarAgendaDia"),
    path('confirmarAgendamentos/', views.confirmarAgendamentos, name="confirmarAgendamentos"),
    path('filtrarAgendamentos/', views.filtrarAgendamentos, name="filtrarAgendamentos"),
    path('filtrarAgendamentosAgendaDia/', views.filtrarAgendamentosAgendaDia, name="filtrarAgendamentosAgendaDia")
]