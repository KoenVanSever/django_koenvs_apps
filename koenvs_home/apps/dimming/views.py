from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.conf import settings
# ! imported for image rendering
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt
import io
import os
import pandas as pd
from pandas import read_csv

# * MATPLOTLIB CONFIGURATION
mpl.rcParams["figure.figsize"] = 8, 6
mpl.rcParams["figure.dpi"] = 100
# BASE_DIR = os.getcwd()
# target_file = os.path.join(BASE_DIR, "temporary/rcParams.txt")
# with open(target_file, "w") as f:
#     for k, v in mpl.rcParams.items():
#         f.write(f"{k}: {v}\n")

# Create your views here.


def split_base_ext_series(pd_ser):
    base = []
    ext = []
    for x in pd_ser:
        temp = os.path.splitext(x)
        base.append(temp[0])
        ext.append(temp[1])
    return base, ext


def plot_ser(ax, abs_path_plot_list):
    for x in abs_path_plot_list:
        df = read_csv(x)
        # TODO: clean this up
        ax.plot(df.input, df.output, label=os.path.basename(x).split(".")[0])


def dimmingIndex(request):
    # * GETTING DATA AND CONSTRUCTING CONTEXT
    target_directory = os.path.join(
        settings.STATICFILES_DIRS[0], "data/dimming/")
    target_file = os.path.join(
        settings.STATICFILES_DIRS[0], "media/temporary/temp.svg")
    full_dirlist = pd.DataFrame()
    full_dirlist["listdir"] = os.listdir(target_directory)
    full_dirlist["full_path"] = [os.path.join(
        target_directory, x) for x in full_dirlist["listdir"]]
    full_dirlist["basename"], full_dirlist["ext"] = split_base_ext_series(
        full_dirlist["listdir"])
    csv_dirlist = full_dirlist[full_dirlist["ext"] == ".csv"]
    csvfiles = list(
        csv_dirlist["basename"])

    # * ACTING ON USER INPUT
    if request.method == "GET":
        fig, ax = plt.subplots(1, 1)
        ax.legend()
        fig.savefig(target_file)
    elif request.method == "POST":
        requested = request.POST.getlist("check")
        # TODO: clean this up
        req_full = list(list(csv_dirlist.loc[csv_dirlist["basename"] == x]
                             ["full_path"])[0] for x in requested)
        fig, ax = plt.subplots(1, 1)
        plot_ser(ax, req_full)
        ax.legend()
        fig.savefig(target_file)
    return render(request, "dimming/index.html", {"csvfiles": csvfiles})

# ! ---------------------------
# ! UNDER DEVELOPMENT / TESTING
# ! ---------------------------


def setPlt():
    # /i put your image actions in the plt quick approach
    plt.clf()
    x = [1, 2, 3, 4, 5]
    y = [10, 5, 8, 4, 7]
    plt.plot(x, y, label="method2")


def pltToSvg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s


def test(request, method):
    # /i first method of plotting in django using matplotlib (using FigureCanvas from backend_agg)
    # /i seen this before however a bit annoying since your HTTP response is the image (nothing else on the page)
    # /i maybe you can pass through context into image
    if method == 1:
        fig = Figure()
        ax = fig.add_subplot(111)
        x = [1, 2, 3, 4, 5]
        y = [10, 5, 8, 4, 7]
        ax.plot(x, y, '-', label="method1")
        canvas = FigureCanvas(fig)
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response)
        return response
    # /i second method: buffer data in io object bytes format (abso to pass through context?)
    elif method == 2:
        setPlt()  # create the plot
        svg = pltToSvg()  # convert plot to SVG
        plt.cla()  # clean up plt so it can be re-used
        response = HttpResponse(svg, content_type='image/svg+xml')
        return response
    # /i third method: make a temporary image
    elif method == 3:
        if os.path.exists("static/media/temporary/test.svg"):
            os.remove("static/media/temporary/test.svg")
        plt.clf()
        x = [1, 2, 3, 4, 5]
        y = [10, 5, 8, 4, 7]
        plt.plot(x, y, label="method3")
        plt.savefig("static/media/test.svg")
        return render(request, "dimming/test.html")
    else:
        return HttpResponse("Not a valid option")
