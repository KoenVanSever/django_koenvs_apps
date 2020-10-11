from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

# Create your views here.


def magneticsIndex(request):
    return render(request, "magnetics/index.html")
