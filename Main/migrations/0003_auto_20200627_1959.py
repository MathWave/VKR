# Generated by Django 3.0.2 on 2020-06-27 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Main", "0002_auto_20200626_0946"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscribe",
            name="is_assistant",
            field=models.IntegerField(default=0),
        ),
    ]
