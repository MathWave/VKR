# Generated by Django 3.2.4 on 2022-02-11 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0019_set_auto_add_new_languages'),
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageApply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_id', models.IntegerField()),
                ('applied', models.BooleanField(default=False)),
            ],
        ),
    ]
