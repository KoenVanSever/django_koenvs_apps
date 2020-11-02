from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def homeIndex(request):
    request.session["main_height"] = 700
    return render(request, "index.html")
