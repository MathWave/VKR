# Generated by Django 3.2.4 on 2022-05-09 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0035_remove_task_memory_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='memory_limit',
            field=models.IntegerField(default=524288),
        ),
    ]
