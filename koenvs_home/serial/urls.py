from django.urls import path
from . import views

app_name = 'serial'
urlpatterns = [
    path('', views.serialIndex, name = "index"),
]
