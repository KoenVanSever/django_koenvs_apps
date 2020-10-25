from django.urls import path
from . import views

app_name = 'params'
urlpatterns = [
    path('', views.paramsIndex, name="index"),
    path('detail/<int:param_id>', views.paramsDetail, name="detail"),
]
