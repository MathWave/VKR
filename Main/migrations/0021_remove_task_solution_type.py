# Generated by Django 3.1 on 2020-10-08 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Main", "0020_task_solution_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="solution_type",
        ),
    ]
