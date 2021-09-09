# Generated by Django 3.2.5 on 2021-08-08 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0053_auto_20210809_0032'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.TextField()),
                ('is_test', models.BooleanField()),
                ('file', models.FileField(upload_to='files')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.task')),
            ],
        ),
    ]