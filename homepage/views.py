import os

from django.shortcuts import render

# Create your views here.
def index(request):
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  print(BASE_DIR)
  return render(request, 'homepage/homepage.html')