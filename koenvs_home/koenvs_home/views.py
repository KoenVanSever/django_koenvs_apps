from django.http import HttpResponse

# Create your views here.
def homeIndex(request):
    return HttpResponse("This is home")