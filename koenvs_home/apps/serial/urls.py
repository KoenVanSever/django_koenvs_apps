from django.urls import path
from . import views

app_name = 'serial'
urlpatterns = [
    path('', views.serialIndex, name="index"),
    path('testdb', views.TestDbListView.as_view(), name="test_db"),
    path('testdb/<int:conv_id>', views.ConvExtraInfo, name="test_db_extra")
]
