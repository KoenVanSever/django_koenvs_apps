from django.shortcuts import render, redirect
from django.http import FileResponse
from .models import Parameter
from json import loads, dumps
from pathlib import Path
# Create your views here.


def get_default_params():
    default = Parameter()
    def_tuple = default.get_four_way_tuple()
    params_default = {}
    for e in def_tuple:
        params_default[e[1]] = e[2]
    return dumps(params_default)


CAT_CHOICES = [x[0] for x in Parameter.cat_choices] + [""]
DEFAULT_PARAMS = get_default_params()


def paramsIndex(request):
    """ Dipslays self made index page for params application """
    if not request.session.get("default_params"):
        request.session["default_params"] = DEFAULT_PARAMS
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
        tuples = obj.get_four_way_tuple()

        return render(request, "params/detail.html", {"param_id": param_id, "tuples": tuples, "text_info": text_info, "process_message": message})
