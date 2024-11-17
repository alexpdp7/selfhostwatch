from django.views.generic import ListView

from shw.dj.updates import models


class AppUpdatesListView(ListView):
    def get_queryset(self):
        return models.Update.objects.filter(name=self.kwargs["name"]).order_by("-date")
