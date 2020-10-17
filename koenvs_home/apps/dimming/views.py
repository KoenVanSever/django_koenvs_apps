from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
# ! imported for image rendering
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import io
import os


# Create your views here.
def dimmingIndex(request):
    return render(request, "dimming/index.html")

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
    elif method == 2:
        setPlt()  # create the plot
        svg = pltToSvg()  # convert plot to SVG
        plt.cla()  # clean up plt so it can be re-used
        response = HttpResponse(svg, content_type='image/svg+xml')
        return response
    elif method == 3:
        if os.path.exists("static/media/test.svg"):
            os.remove("static/media/test.svg")
        plt.clf()
        x = [1, 2, 3, 4, 5]
        y = [10, 5, 8, 4, 7]
        plt.plot(x, y, label="method3")
        plt.savefig("static/media/test.svg")
        return render(request, "dimming/test.html")
    else:
        return HttpResponse("Not a valid option")
