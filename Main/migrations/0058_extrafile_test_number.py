# Generated by Django 3.2.5 on 2021-08-13 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0057_alter_extrafile_is_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='extrafile',
            name='test_number',
            field=models.IntegerField(null=True),
        ),
    ]
