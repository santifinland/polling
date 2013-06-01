from django.core.context_processors import request
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

