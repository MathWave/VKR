# Generated by Django 3.2.4 on 2021-09-02 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0068_userinfo_telegram_chat_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='telegram_chat_id',
        ),
    ]
