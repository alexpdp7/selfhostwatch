from django.db import models


class Architecture(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


BOOLEAN_FEATURE_CHOICES = (
    ("true", "true"),
    ("false", "false"),
    ("not_relevant", "not_relevant"),
)


class AppVersion(models.Model):
    name = models.CharField(max_length=100)
    architectures = models.ManyToManyField(Architecture)
    version = models.CharField(max_length=100)
    yuno_ldap = models.CharField(max_length=20, choices=BOOLEAN_FEATURE_CHOICES)
    yuno_multi_instance = models.CharField(
        max_length=20, choices=BOOLEAN_FEATURE_CHOICES
    )
    yuno_sso = models.CharField(max_length=20, choices=BOOLEAN_FEATURE_CHOICES)
    yuno_high_quality = models.BooleanField(blank=True, null=True)
    yuno_maintained = models.BooleanField(blank=True, null=True)
    yuno_state = models.CharField(max_length=100)
    repo = models.CharField(max_length=100, blank=True, null=True)
    updated = models.DateTimeField()

    def __str__(self):
        return self.name
