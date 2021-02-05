from django.urls import path
from . import views

app_name = 'dimming'
urlpatterns = [
    path('', views.dimmingIndex, name="index"),
    path('test/<int:method>/', views.test, name="test"),
    path('ajax/', views.ajax_view, name="ajax"),
]
