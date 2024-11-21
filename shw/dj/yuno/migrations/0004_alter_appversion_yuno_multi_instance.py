# Generated by Django 5.1.2 on 2024-11-19 19:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("yuno", "0003_appversion_repo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appversion",
            name="yuno_multi_instance",
            field=models.CharField(
                choices=[
                    ("true", "true"),
                    ("false", "false"),
                    ("not_relevant", "not_relevant"),
                ],
                max_length=20,
            ),
        ),
    ]
