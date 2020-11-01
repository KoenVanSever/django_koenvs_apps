def store_general_session(request):
    if "height" in request.POST.keys():
        request.session["main_height"] = int(request.POST["height"])
    if "width" in request.POST.keys():
        request.session["main_width"] = int(request.POST["width"])
    return request
