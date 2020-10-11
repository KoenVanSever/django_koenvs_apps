from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from static.my_modules.safeserial import SafeSerial as Sfs  # pylint: disable=import-error

# Create your views here.
SER = Sfs()  # /i MAIN SER OBJECT


def serialIndex(request):
    return render(request, "serial/index.html")
