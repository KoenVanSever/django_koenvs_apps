from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from .models import Converter, LedCalib, CcrCalib
from django.http import HttpResponse
from static.my_modules.safeserial import SafeSerial as Sfs  # pylint: disable=import-error
from json import dumps, dump, loads
import serial.tools.list_ports as stl  # pylint: disable=import-error disable=no-name-in-module
from time import sleep
import sys
from datetime import date

# * STARTUP FUNCTIONS

def get_init_pid():
    today = date.today().isocalendar()
    year = str(today[0])[-2:]
    week = str(today[1])
    week = "0" + week if len(week) < 2 else week
    supp = "04"
    sn = "0000001"
    return (year + week + supp + sn)


def gen_ports_list():
    ports_list = stl.comports()
    ser_ports = []
    for i in range(len(ports_list)):
        ser_ports.append(
            f"{ports_list[i].device}  -  {ports_list[i].description}")
    return ports_list, ser_ports


# * DATA OBJECTS FOR START
# ! THESE ARE GLOBAL VARIABLES, TAKE CARE WITH GLOBAL SCOPE WITHIN FUNCTIONS

_, ports_list = gen_ports_list()
ser = Sfs()  # /i MAIN SER OBJECT
ser.close()  # /i close port by default when starting application
start_port = ""
if sys.platform == "linux":
    for temp in ports_list:
        if "USB" in temp:
            start_port = temp 
else:
    start_port = ports_list[0]
entry_data = {"arg1": 5, "arg2": 3, "conv": "HPC",
              "sel_port": start_port, "command": "", "buf_time_man": "", "manual": False, "ledcalib_state": ["off", 0], "pid": get_init_pid()}
terminal_text = [""]
prefix = ""
# with open("temporary/test.json", "w") as f:
#     dump({"entry_data": entry_data, "ser_ports": ports_list}, f, indent=2)


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
    global prefix
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


def append_term(command, wait=0.05):
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


def hpc_fo_comm(hpc_comm, fo_comm, hpc_wait = 0.1, fo_wait = 0.1):
    """ HPC and FO behavior is different for certain command """
    if entry_data["conv"] == "HPC":
        append_term(str(hpc_comm), float(hpc_wait))
    elif entry_data["conv"] == "FO/LCC":
        append_term(str(fo_comm), float(fo_wait))
    else:
        terminal_text.append(prefix + "Command not send, please specify converter type")


def serialIndex(request):
    global entry_data
    global terminal_text

    if request.method == "GET":
        if ser.is_open:
            ser.reset_input_buffer() # ! necessary?
        entry_data["command"] = "" # /i always reset command to nothing
        entry_data["manual"] = False # /i always reset manual to False
        terminal_text = [""]
        return render_ser_index(request)
    elif request.method == "POST":
        if ser.is_open:
            ser.reset_input_buffer() # ! necessary?
        # TODO: help with shortened buffer time still gives issues on following command (input buffer still seems to have data?)
        entry_data = loads(request.POST["data"])
        manual_command_handle = entry_data["manual"]
        entry_data["manual"] = False # /i always reset manual to False
        print(entry_data)
        comm_proc = entry_data["command"]
        sel_port = entry_data["sel_port"].split("-")[0].rstrip()
        # print(comm_proc)

        if not ser.is_open:
            on_ser_closed(request, comm_proc, sel_port)

        elif ser.is_open:
            if ser.port == sel_port:

                if manual_command_handle:
                    try:
                        buftime = float(entry_data["buf_time_man"])
                    except ValueError:
                        append_term(comm_proc, 0.1)
                    else:
                        append_term(comm_proc, buftime)

                # * General commands
                elif comm_proc == "open":
                    on_ser_open_open()
                elif comm_proc == "clear":
                    terminal_text = ["", "Terminal cleared, port still open."]
                elif comm_proc == "exit":
                    # ser.write_reg("exit")
                    # sleep(0.05)
                    # ret = ser.read_print_buffer()
                    ser.close()
                    terminal_text.append("Port closed")
                elif comm_proc == "getver":
                    hpc_fo_comm("hwrev", "getver")
                elif comm_proc == "readvolt":
                    append_term("readvolt")
                elif comm_proc == "help":
                    ser.write_reg("help")
                    reps = 5 if entry_data["conv"] == "FO/LCC" else 12
                    i = 0
                    endstring = ""
                    while i < reps:
                        sleep(0.2)
                        endstring += ser.read_print_buffer()
                        i += 1
                    buf = endstring.split("\n")
                    buf.pop()
                    terminal_text.append(prefix + buf[0])
                    terminal_text = terminal_text + buf[1:]
                elif comm_proc == "recvtest":
                    append_term("recvtest", 1.2)

                # * ccr commands
                elif comm_proc == "getccr":
                    hpc_fo_comm("getCCRcurrent", "getccr")
                elif comm_proc == "calibccrlo 2000":
                    hpc_fo_comm("calibCCRlo 2000", "calibccrlo 2000", 0.05, 1.1)
                elif comm_proc == "calibccrhi 6600":
                    hpc_fo_comm("calibCCRhi 6600", "calibccrlo 6600", 0.05, 1.1)
                elif comm_proc == "calibccrsave":
                    hpc_fo_comm("calibCCRsave yes", "calibccrsave yes")
                elif comm_proc == "getcalib":
                    append_term("getcalib")

                # * led commands
                elif comm_proc == "ledinfo":
                    sending = f"ledinfo {entry_data['arg1']} {entry_data['arg2']}"
                    append_term(sending, 0.2)
                elif comm_proc == "ledcalib":
                    # terminal_text.append("Not implemented yet")
                    # TODO: implement ledcalib correctly? --> TEST FUNCTIONALITY IN REAL LIFE (FO / HPC)
                    if not (str(entry_data["arg1"]) in ("1", "4")):
                        terminal_text.append("Please set arg1 to 1 or 4")
                    else:
                        if entry_data["ledcalib_state"][0] == "off":
                            sending = f"ledcalib {entry_data['arg1']}"
                            append_term(sending, 0.5)
                            entry_data["ledcalib_state"] = ["low", 0]
                        elif entry_data["ledcalib_state"][0] == "low":
                            sending = str(entry_data["ledcalib_state"][1])
                            append_term(sending, 0.2)
                            entry_data["ledcalib_state"] = ["high", 0]
                        elif entry_data["ledcalib_state"][0] == "high":
                            sending = str(entry_data["ledcalib_state"][1])
                            append_term(sending, 0.2)
                            entry_data["ledcalib_state"] = ["off", 0]
                elif comm_proc == "getledcalib":
                    sending = f"getledcalib {entry_data['arg1']}"
                    append_term(sending)
                elif comm_proc == "ledinactivate":
                    sending = f"ledinactivate {entry_data['arg1']}"
                    append_term(sending, 1.2)
                elif comm_proc == "getledstatus":
                    sending = f"getledstatus {entry_data['arg1']}"
                    append_term(sending, 0.4)
                elif comm_proc == "setledovr":
                    sending = f"setledovr {entry_data['arg1']} {entry_data['arg2']}"
                    append_term(sending)
                elif comm_proc == "setledovr2":
                    sending = f"setledovr2 {entry_data['arg1']} {entry_data['arg2']}"
                    append_term(sending)
                
                # * asp
                elif comm_proc == "rx":
                    # TODO: implement rx functionality correctly --> timing of buffer? ploting results (in dialog)?
                    terminal_text.append("Not implemented yet")
                elif comm_proc == "asp on":
                    append_term("asp on")
                elif comm_proc == "asp off":
                    append_term("asp off")
                elif comm_proc == "setTXpower":
                    sending = f"setTXpower {entry_data['arg1']}"
                    append_term(sending)
                elif comm_proc == "params dump":
                    append_term("params dump", 0.5)
                elif comm_proc == "getPID":
                    append_term("getPID", 0.1)
                elif comm_proc == "setPID":
                    # DONE: take PID entry field and implement code for PID programmation of PCBAs..
                    sending = f"setPID {entry_data['pid']}"
                    append_term(sending, 0.3)
                    sleep(0.05)
                    ser.write("yes\r".encode("utf8"))
                    sleep(0.1)
                    read = ser.read_print_buffer()
                    terminal_text = terminal_text + read.split("\n")

                # * not implemented
                else:
                    terminal_text.append("Command not implemented yet")

            else:
                if comm_proc == "exit":
                    ser.close()
                    terminal_text.append("Port closed")
                else:
                    terminal_text.append("Opened port and selected port are different, please specify right port!")

        # print(terminal_text)
        return render_ser_index(request)

# ! ---------------------------
# ! UNDER DEVELOPMENT / TESTING
# ! ---------------------------

class TestDbListView(ListView):
    # model = Converter # /i not needed when you use queryset?
    template_name = "serial/test_db.html" # /i this template is sought instead in template dirs, instead of the default one
    context_object_name = "test_list" # /i this name can be used inside the template to cycle through or whatever (instead of default)

    def get_queryset(self):
        """ This returns a list of objects to our specification instead of default """
        return (Converter.objects.all()) #pylint: disable=no-member

def ConvExtraInfo(request, conv_id):
    conv = get_object_or_404(Converter, pk = conv_id)
    try:
        ledc = LedCalib.objects.filter(conv_id = conv.id) #pylint: disable=no-member
        ccrc = CcrCalib.objects.filter(conv_id = conv.id) #pylint: disable=no-member
    except (KeyError, LedCalib.DoesNotExist, CcrCalib.DoesNotExist): #pylint: disable=no-member
        return render(request, "serial/conv_info.html", {"converter": conv, "error_message": "No LED calib or CCR calib information found"})
    else:
        return render(request, "serial/conv_info.html", {"converter": conv, "ledcalib": ledc, "ccrcalib": ccrc})
