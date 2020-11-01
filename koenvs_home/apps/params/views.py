from django.shortcuts import render, redirect
from django.http import FileResponse
from .models import Parameter
from json import loads
from pathlib import Path
from static.koenvs_modules.general import store_general_session
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
    request = store_general_session(request)
    print(request.session["main_height"])
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
    request = store_general_session(request)
    if request.method == "GET":
        return redirect("/params/", permanent=True)
    elif request.method == "POST":
        # - Determine sizing of different fields
        rows = (request.session["main_height"] - 60) // 44
        message = ""

        # - Handle export csv and save db
        if "export" in request.POST:
            # /i get data
            target_csv_name = request.POST["csv_entry"]
            target_short_name = request.POST["short_entry"]
            target_cat = request.POST["cat_entry"]
            target_data = loads(request.POST["data"])
            target_data = dict([(k, int(v)) for k, v in target_data.items()])

            # /i handle action in model
            search_csv = Parameter.objects.filter(csv_name=target_csv_name)
            if search_csv.exists():
                temp = search_csv[0]
                temp.short_name = target_short_name
                temp.category = target_cat
                temp.update_data_without_save(target_data)
                temp.save()
                message = "Existing parameter file saved"
            else:
                new = Parameter(csv_name=target_csv_name,
                                short_name=target_short_name, category=target_cat)
                new.update_data_without_save(target_data)
                new.save()
                param_id = new.id
                message = "New parameter file created"

            if request.POST["export"] == "export_csv":
                temp = Parameter.objects.get(csv_name=target_csv_name)
                target_dir = Path(__file__, "..", "..", "..",
                                  "temporary", "generated").resolve()
                message = "File generated"
                for x in target_dir.iterdir():
                    x.unlink()
                return FileResponse(open(temp.create_file(target_dir), "rb"), as_attachment=True, filename=temp.csv_name)

        # - prepare context
        obj = Parameter.objects.get(pk=param_id)
        text_info = {"csv_name": obj.csv_name,
                     "short_name": obj.short_name, "category": obj.category}
        tuples = obj.get_three_way_tuple()
        split = split_tuples(tuples, rows)
        return render(request, "params/detail.html", {"param_id": param_id, "split": split, "text_info": text_info, "process_message": message})
