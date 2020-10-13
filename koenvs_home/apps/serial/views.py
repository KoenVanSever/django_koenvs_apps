from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from static.my_modules.safeserial import SafeSerial as Sfs  # pylint: disable=import-error
from json import dumps, dump, loads
import serial.tools.list_ports as stl  # pylint: disable=import-error disable=no-name-in-module
from time import sleep


def gen_ports_list():
    ports_list = stl.comports()
    ser_ports = []
    for i in range(len(ports_list)):
        ser_ports.append(
            f"{ports_list[i].device}  -  {ports_list[i].description}")
    return ports_list, ser_ports


# * DATA OBJECTS FOR START
# ! THESE ARE GLOBAL VARIABLES, TAKE CARE WITH GLOBAL SCOPE WITHIN FUNCIONS

_, ports_list = gen_ports_list()
ser = Sfs()  # /i MAIN SER OBJECT
ser.close()  # /i close port by default when starting application
entry_data = {"arg1": 5, "arg2": 3, "conv": "HPC",
              "sel_port": ports_list[0], "command": ""}
terminal_text = [""]
prefix = ""
# with open("temporary/test.json", "w") as f:
#     dump({"entry_data": dumps(entry_data), "ser_ports": ports_list}, f)


# * Create your views here.

def on_ser_closed(request, comm_proc, sel_port):
    """ Does actions when port is closed upon button click """
    global prefix
    if comm_proc == "open":
        ser.close()
        ser.port = sel_port
        try:
            ser.open()
        except Exception:
            terminal_text.append("Selected port invalid")
            return render_ser_index(request)
        read = ser.open_admin()
        if "(3)" in read:
            prefix = read.split("\n")[1]
            terminal_text.append("Terminal opened on correct level!")
        else:
            terminal_text.append("Something went wrong!")
    elif comm_proc == "exit":
        terminal_text.append("Port is already closed")
    else:
        terminal_text.append(
            "Please open the terminal with the correct port selected")


def on_ser_open_open():
    """Does the actions of the serial port and terminal printing when serial port is open"""
    ser.write_reg("open")
    sleep(0.05)
    ret = ser.read_print_buffer()
    if "(3)" in ret:
        terminal_text.append(
            "Terminal opened on correct level!")
    else:
        i = 0
        while i < 2:
            ret = ser.open_admin()
            if "(3)" in ret:
                prefix = ret.split("\n")[1]
                terminal_text.append(
                    "Terminal opened on correct level!")
                break
            i += 1


def append_resp(command, wait=0.05):
    """ Sends command and changes resp to page """
    global terminal_text
    ser.write_reg(command)
    sleep(wait)
    buf = ser.read_print_buffer().split("\n")
    terminal_text.append(prefix + buf[0].rstrip())
    n = len(buf)
    terminal_text = terminal_text + buf[1:n-1]
    return None


def render_ser_index(request):
    global entry_data
    global terminal_text
    global ports_list
    entry_data["command"] = ""
    return render(request, "serial/index.html", {"entry_data": dumps(entry_data), "ser_ports": ports_list, "terminal_text": terminal_text})


def serialIndex(request):
    global entry_data
    global terminal_text
    if request.method == "GET":
        entry_data["command"] = ""
        terminal_text = [""]
        return render_ser_index(request)
    elif request.method == "POST":

        entry_data = loads(request.POST["data"])
        print(entry_data)
        comm_proc = entry_data["command"]
        sel_port = entry_data["sel_port"].split("-")[0].rstrip()
        # print(comm_proc)

        if not ser.is_open:
            on_ser_closed(request, comm_proc, sel_port)

        elif ser.is_open:
            if ser.port == sel_port:
                if comm_proc == "open":
                    on_ser_open_open()
                elif comm_proc == "clear":
                    terminal_text = [""]
                elif comm_proc == "exit":
                    # ser.write_reg("exit")
                    # sleep(0.05)
                    # ret = ser.read_print_buffer()
                    ser.close()
                    terminal_text.append("Port closed")
                elif comm_proc == "getver":
                    append_resp("getver")
                elif comm_proc == "readvolt":
                    append_resp("readvolt")
            else:
                terminal_text.append(
                    "Opened port and selected port are different, please specify right port!")

        # print(terminal_text)
        return render_ser_index(request)
