# Generated by Django 3.2.4 on 2022-02-16 07:33

import Checker.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Checker', '0004_alter_checker_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='checker',
            name='dynamic_token',
            field=models.CharField(db_index=True, default=Checker.models.generate_token, max_length=30, unique=True),
        ),
    ]
