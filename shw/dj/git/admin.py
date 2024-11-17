from django.contrib import admin

from shw.dj.git import models


admin.site.register(models.GitApp)
admin.site.register(models.Version)
