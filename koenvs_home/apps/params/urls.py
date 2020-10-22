from django.urls import path
from . import views

app_name = 'params'
urlpatterns = [
    path('', views.paramsIndex, name="index"),
]
