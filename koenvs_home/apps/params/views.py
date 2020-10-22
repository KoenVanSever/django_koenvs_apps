from django.shortcuts import render

# Create your views here.


def paramsIndex(request):
    return render(request, "params/index.html")
