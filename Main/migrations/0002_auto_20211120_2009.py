# Generated by Django 3.2.4 on 2021-11-20 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='verified',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='code',
            field=models.IntegerField(null=True),
        ),
    ]
