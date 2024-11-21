from django.urls import path

from . import views

urlpatterns = [
    path("index.html", views.AppListView.as_view()),
    path("app/<slug:name>.html", views.AppUpdatesListView.as_view()),
]
