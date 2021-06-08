from django.shortcuts import render,get_object_or_404


def index(request):
  return render(request, 'COVID/covid.html')

def world_TC(request):
  return render(request, 'COVID/world_TC.html')

def world_NC(request):
  return render(request, 'COVID/world_NC.html')

def world_TD(request):
  return render(request, 'COVID/world_TD.html')

def world_ND(request):
  return render(request, 'COVID/world_ND.html')


