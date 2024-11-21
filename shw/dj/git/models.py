from django.db import models


class GitApp(models.Model):
    name = models.CharField(max_length=100)
    remote_url = models.CharField(max_length=100)
    manual = models.BooleanField(help_text="Do not update automatically", default=True)

    def __str__(self):
        return self.name


class Version(models.Model):
    git_app = models.ForeignKey(GitApp, on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.git_app}-{self.version}"
