# Generated by Django 5.1.2 on 2024-11-19 18:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("yuno", "0002_alter_appversion_yuno_high_quality_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="appversion",
            name="repo",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
