from django.db import models


class Update(models.Model):
    source = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    date = models.DateTimeField()
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
