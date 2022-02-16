# Generated by Django 3.2.4 on 2022-02-15 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0020_languageapply'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.set'),
        ),
        migrations.AddIndex(
            model_name='solution',
            index=models.Index(fields=['set', '-time_sent'], name='Main_soluti_set_id_19e6c7_idx'),
        ),
    ]
