from django.urls import path
from . import views

urlpatterns = [
    path('cadastrarAgendamentos/', views.cadastrarAgendamentos, name="cadastrarAgendamentos")
]