# Generated by Django 3.2.4 on 2022-02-22 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0022_auto_20220217_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='enter_token',
            field=models.CharField(max_length=30, null=True),
        ),
    ]