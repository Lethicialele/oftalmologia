from django.shortcuts import redirect
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('cadastrarMedicos/', views.cadastrarMedicos, name="cadastrarMedicos"),
    path('cadastrarPacientes/', lambda request: redirect('cadastrarPacientes', permanent=True)),
    path('cadastrarPacientes/', lambda request: redirect('cadastrarPacientes', permanent=True)),
    path('cadastrarMedicos/', lambda request: redirect('cadastrarMedicos', permanent=True)),
    path('loginMedicos/', views.loginMedicos, name='loginMedicos'),
    path('cadastrarAgendamentos/', lambda request: redirect('cadastrarAgendamentos', permanent=True)),
    path('cadastrarProcedimentos/', lambda request: redirect('cadastrarProcedimentos', permanent=True)),
    path('consultarAgendaDia/', lambda request: redirect('consultarAgendaDia', permanent=True)),
    path('home', lambda request: redirect('', permanent=True)),
    path('atualizarCadastrorMedicos/', views.atualizarCadastrorMedicos, name="atualizarCadastrorMedicos"),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]