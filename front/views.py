from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.http import HttpResponse


def index(request):
    return redirect("http://localhost:5000")
    #return HttpResponse("Hello, world. You're at the Sogang univ. Ballotchain team.")