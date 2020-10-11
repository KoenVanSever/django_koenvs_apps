from django.urls import path
from . import views

app_name = 'magnetics'
urlpatterns = [
    path('', views.magneticsIndex, name="index"),
]
