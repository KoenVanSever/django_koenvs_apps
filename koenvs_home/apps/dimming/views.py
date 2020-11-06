from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .forms import UploadFileForm
from json import dumps, dump, loads
# ! imported for image rendering
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt
import io
import os
import pandas as pd
from pandas import read_csv
from pathlib import Path

# ! HIGH LEVEL ACTIONS:
# TODO: put context on webpage so that it remembers which lines were selected and formats page in such a way that it is visibles


# * MATPLOTLIB CONFIGURATION
mpl.rcParams["figure.figsize"] = 8, 6
mpl.rcParams["figure.dpi"] = 100
mpl.rcParams["axes.grid"] = True
# BASE_DIR = os.getcwd()
# target_file = os.path.join(BASE_DIR, "temporary/rcParams.txt")
# with open(target_file, "w") as f:
#     for k, v in mpl.rcParams.items():
#         f.write(f"{k}: {v}\n")
# * GLOBAL DIRECTORY SETUP
# TODO: clean this shit up with patlib instead of os.path
target_directory = Path(
    settings.STATICFILES_DIRS[0], "data", "dimming", "generated")
limit_directory = Path(
    settings.STATICFILES_DIRS[0], "data", "dimming", "limits")
target_file = Path(
    settings.STATICFILES_DIRS[0], "media", "temporary", "temp.svg")


def create_base_fig_ax():
    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel("Input current (Arms)")
    ax.set_ylabel("Relative intensity (%)")
    ax.set_xticks([2.4, 2.8, 3.1, 3.4, 3.8, 4.1,
                   4.5, 4.8, 5.2, 5.5, 5.8, 6.2, 6.6])
    ax.set_xlim([2.3, 6.8])
    ax.set_ylim([-5, 105])
    ax.set_title("Dimming curve plot")
    return fig, ax


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


def refresh_files_list(target_dir):
    full_dirlist = pd.DataFrame()
    full_dirlist["listdir"] = os.listdir(target_dir)
    full_dirlist["full_path"] = [os.path.join(
        target_dir, x) for x in full_dirlist["listdir"]]
    full_dirlist["basename"], full_dirlist["ext"] = split_base_ext_series(
        full_dirlist["listdir"])
    csv_dirlist = full_dirlist[full_dirlist["ext"] == ".csv"]
    csvfiles = sorted(list(
        csv_dirlist["basename"]))
    return csv_dirlist, csvfiles


@require_http_methods(["GET", "POST"])
def dimmingIndex(request):
    # * GETTING DATA AND CONSTRUCTING CONTEXT
    csv_dirlist, csvfiles = refresh_files_list(target_directory)
    limit_dirlist, limitfiles = refresh_files_list(limit_directory)
    selected = []

    # * ACTING ON USER INPUT
    if request.method == "GET":
        fig, ax = create_base_fig_ax()
        ax.legend(loc="upper left")
        fig.savefig(target_file)
        # file_form = UploadFileForm()
    elif request.method == "POST":
        # print(request.POST)
        if ("check_files" in request.POST.keys()) or ("check_limits" in request.POST.keys()):
            requested_files = request.POST.getlist("check_files")
            requested_limits = request.POST.getlist("check_limits")
            # TODO: clean this up
            req_files = list(list(csv_dirlist.loc[csv_dirlist["basename"] == x]
                                  ["full_path"])[0] for x in requested_files)
            req_limits = list(list(limit_dirlist.loc[limit_dirlist["basename"] == x]
                                   ["full_path"])[0] for x in requested_limits)
            req_full = req_files + req_limits
            selected = dumps([os.path.basename(x).split(".")[0]
                              for x in req_full])
            fig, ax = create_base_fig_ax()
            plot_ser(ax, req_full)
            ax.legend(loc="upper left")
            fig.savefig(target_file)
        elif "file_input" in request.FILES.keys():
            # file_form = UploadFileForm(request.POST, request.FILES)
            myfiles = request.FILES.getlist('file_input')
            fs = FileSystemStorage(location=target_directory)
            for file in myfiles:
                if file.name in list(csv_dirlist["listdir"]):
                    continue
                fs.save(file.name, file)
            csv_dirlist, csvfiles = refresh_files_list(
                target_directory)
        elif "file_other" in request.POST.keys():
            for file in csv_dirlist["full_path"]:
                # print(file)
                os.remove(file)
            csv_dirlist, csvfiles = refresh_files_list(target_directory)
    return render(request, "dimming/index.html", {"csvfiles": csvfiles, "limitfiles": limitfiles, "selected": selected})
    # return render(request, "dimming/index.html", {"csvfiles": csvfiles, "file_form": file_form.as_p()})

# ! ------------------------------
# ! UNDER DEVELOPMENT / TESTING --
# ! ------------------------------


def ajax_view(request):
    print(request)
    return JsonResponse({"x": "blabla"})


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
