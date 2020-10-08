from django.urls import path

from . import views

app_name = "app01" # kind of like namespacing if you have different apps
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name="detail"),
    # what's passed the get starting from app01/, file.function, name
    path('<int:question_id>/results/', views.results, name="results"),
    path('<int:question_id>/vote/', views.vote, name="vote"),
]