# Generated by Django 3.1.3 on 2021-01-30 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Main", "0028_task_show_result"),
    ]

    operations = [
        migrations.AddField(
            model_name="block",
            name="priority",
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name="task",
            name="priority",
            field=models.IntegerField(default=5),
        ),
    ]
