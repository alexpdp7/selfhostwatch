from django.contrib import admin

from shw.dj.git import models


class VersionAdmin(admin.ModelAdmin):
    list_display = ["git_app__name", "version", "date"]


admin.site.register(models.GitApp)
admin.site.register(models.Version, VersionAdmin)
