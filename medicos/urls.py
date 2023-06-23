from django.urls import path
from . import views

urlpatterns = [
    path('cadastrarMedicos/', views.cadastrarMedicos, name="cadastrarMedicos")
]