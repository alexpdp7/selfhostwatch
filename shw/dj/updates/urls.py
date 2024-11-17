from django.urls import path

from . import views

urlpatterns = [
    path("<slug:name>/", views.AppUpdatesListView.as_view()),
]
