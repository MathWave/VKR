# Generated by Django 3.1 on 2020-09-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0015_auto_20200902_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='max_solutions_count',
            field=models.IntegerField(default=10),
        ),
    ]
