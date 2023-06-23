from django.urls import path
from . import views

urlpatterns = [
    path('cadastrarProcedimentos/', views.cadastrarProcedimentos, name="cadastrarProcedimentos"),
    path('mostrarProcedimentos/', views.mostrarProcedimentos, name="mostrarProcedimentos"),
]