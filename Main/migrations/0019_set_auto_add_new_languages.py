# Generated by Django 3.2.4 on 2022-02-11 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0018_set_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='auto_add_new_languages',
            field=models.BooleanField(default=True),
        ),
    ]
