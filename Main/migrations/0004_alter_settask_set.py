# Generated by Django 3.2.4 on 2021-11-21 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Main", "0003_auto_20211121_2327"),
    ]

    operations = [
        migrations.AlterField(
            model_name="settask",
            name="set",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="settasks",
                to="Main.set",
            ),
        ),
    ]