from django.urls import path
from . import views

app_name = 'dimming'
urlpatterns = [
    path('', views.dimmingIndex, name="index"),
]
