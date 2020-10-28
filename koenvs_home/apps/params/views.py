from django.shortcuts import render, redirect
from .models import Parameter
# Create your views here.

CAT_CHOICES = [x[0] for x in Parameter.cat_choices] + [""]


def split_tuples(tuples, amount):
    split = []
    for x in range(len(tuples)):
        mod = x % amount
        li = x // amount
        if mod == 0:
            split.append([])
        split[li].append(tuples[x])
    return split


def paramsIndex(request):
    """ Dipslays self made index page for params application """
    parameter_list = Parameter.objects.all().order_by(
        "-category", "csv_name")
    if request.method == "GET":
        return render(request, "params/index.html", {"parameter_list": parameter_list})
    elif request.method == "POST":
        if request.POST["category"] in CAT_CHOICES:
            files = request.FILES.getlist("files_upload")
            for file in files:
                temp = file.read().decode()
                db_entry = Parameter.upload_string(
                    temp, file.name, request.POST["category"])
                db_entry.save()
        else:
            message = "invalid category entry"
            return render(request, "params/index.html", {"parameter_list": parameter_list, "input_message": message})
        return render(request, "params/index.html", {"parameter_list": parameter_list})


def paramsDetail(request, param_id):
    if request.method == "GET":
        return redirect("/params/", permanent=True)
    elif request.method == "POST":
        main_height = int(request.POST["height"]) - 72
        print(main_height)
        rows = main_height // 44
        print(rows)
        obj = Parameter.objects.get(pk=param_id)
        tuples = obj.get_three_way_tuple()
        split = split_tuples(tuples, rows)
        return render(request, "params/detail.html", {"split": split})
