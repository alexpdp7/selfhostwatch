from django.contrib import admin

from shw.dj.yuno import models


class AppVersionAdmin(admin.ModelAdmin):
    list_display = ["name", "version", "updated"]


admin.site.register(models.AppVersion, AppVersionAdmin)
admin.site.register(models.Architecture)
