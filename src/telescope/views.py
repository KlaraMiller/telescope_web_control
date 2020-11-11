from django.shortcuts import render

from django.shortcuts import render
from sensors.models import myData, stargate

def index(request):
    return render(request, 'telescope/index.html')