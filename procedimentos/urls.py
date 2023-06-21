from django.urls import path
from . import views

urlpatterns = [
    path('cadastrarProcedimentos/', views.cadastrarProcedimentos, name="cadastrarProcedimentos")
]