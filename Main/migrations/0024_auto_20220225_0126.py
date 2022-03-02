# Generated by Django 3.2.4 on 2022-02-24 22:26

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0023_group_enter_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='enter_token',
        ),
        migrations.AddField(
            model_name='solution',
            name='extras',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]