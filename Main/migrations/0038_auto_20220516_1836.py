# Generated by Django 3.2.4 on 2022-05-16 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0037_alter_userinfo_telegram_chat_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='notification_email',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='notification_telegram',
            field=models.BooleanField(default=False),
        ),
    ]