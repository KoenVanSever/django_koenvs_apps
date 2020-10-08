from django.urls import path

from . import views

app_name = "app02" # kind of like namespacing if you have different apps
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), # refers to classnames in views, which are subclassed from template classes, classmethod ".as_view()" points to url
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]