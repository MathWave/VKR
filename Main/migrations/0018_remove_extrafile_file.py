# Generated by Django 3.1 on 2020-09-17 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Main", "0017_solution_details"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="extrafile",
            name="file",
        ),
    ]
