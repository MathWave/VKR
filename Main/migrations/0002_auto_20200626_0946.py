# Generated by Django 3.0.2 on 2020-06-26 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Main", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userinfo",
            old_name="group_name",
            new_name="group",
        ),
    ]
