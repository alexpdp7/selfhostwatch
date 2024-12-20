from django.views.generic import ListView

from shw.dj.updates import models


class AppListView(ListView):
    template_name = "updates/app_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_updates"] = models.Update.objects.all().order_by("-date")[0:10]
        return context

    def get_queryset(self):
        return models.Update.objects.values("name").distinct().order_by("name")


class AppUpdatesListView(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app"] = self.kwargs["name"]
        return context

    def get_queryset(self):
        return models.Update.objects.filter(name=self.kwargs["name"]).order_by("-date")
