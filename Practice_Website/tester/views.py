from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Beginning, Middle, Last

def index(request):
    return render(request, 'tester/index.html')
  