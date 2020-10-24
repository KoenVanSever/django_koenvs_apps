from django.shortcuts import render
from .models import Parameter
# Create your views here.


def paramsIndex(request):
    parameter_list = Parameter.objects.all()  # pylint: disable=no-member
    return render(request, "params/index.html", {"parameter_list": parameter_list})
