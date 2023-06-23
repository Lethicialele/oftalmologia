from django.shortcuts import render
from agendamentos.views import *

def home(request):
    return render(request, 'home.html')
