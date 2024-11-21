from django.views.generic import ListView

from shw.dj.updates import models


class AppListView(ListView):
    template_name = "updates/app_list.html"

    def get_queryset(self):
        return models.Update.objects.values("name").distinct().order_by("name")


class AppUpdatesListView(ListView):
    def get_queryset(self):
        return models.Update.objects.filter(name=self.kwargs["name"]).order_by("-date")
