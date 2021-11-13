# Generated by Django 3.2.4 on 2021-11-10 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0074_auto_20211106_1215'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolutionFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField()),
                ('fs_id', models.IntegerField()),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.solution')),
            ],
        ),
        migrations.DeleteModel(
            name='Language',
        ),
        migrations.AddField(
            model_name='extrafile',
            name='fs_id',
            field=models.IntegerField(null=True),
        ),
    ]