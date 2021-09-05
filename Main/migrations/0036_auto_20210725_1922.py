# Generated by Django 3.2.5 on 2021-07-25 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Main", "0035_group_users"),
    ]

    operations = [
        migrations.AddField(
            model_name="set",
            name="tasks",
            field=models.ManyToManyField(to="Main.Task"),
        ),
        migrations.AddField(
            model_name="task",
            name="input_format",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="task",
            name="legend",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="task",
            name="output_format",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="task",
            name="public",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="task",
            name="specifications",
            field=models.TextField(default=""),
        ),
    ]
