# Generated by Django 5.1.2 on 2024-11-18 20:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("git", "0002_alter_version_version"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gitapp",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
