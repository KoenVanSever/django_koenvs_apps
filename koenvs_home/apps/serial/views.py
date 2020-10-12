from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from static.my_modules.safeserial import SafeSerial as Sfs  # pylint: disable=import-error
from json import dumps, dump
import serial.tools.list_ports as stl  # pylint: disable=import-error disable=no-name-in-module

# * HELP FUNCTIONS


def gen_ports_list():
    ports_list = stl.comports()
    ser_ports = []
    for i in range(len(ports_list)):
        ser_ports.append(
            f"{ports_list[i].device}  -  {ports_list[i].description}")
    return ports_list, ser_ports

# * DATA OBJECTS FOR START


_, ports_list = gen_ports_list()
SER = Sfs()  # /i MAIN SER OBJECT
entry_data = {"arg1": 5, "arg2": 3, "conv": "HPC", "sel_port": ports_list[0]}
print(ports_list)
with open("temporary/test.json", "w") as f:
    dump({"entry_data": dumps(entry_data), "ser_ports": ports_list}, f)

# * Create your views here.


def serialIndex(request):
    if request.method == "GET":
        return render(request, "serial/index.html", {"entry_data": dumps(entry_data), "ser_ports": ports_list})
    elif request.method == "POST":
        return HttpResponse(request, "This is a post request")
