# Generated by Django 3.2.4 on 2021-12-19 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Main', '0008_userinfo_notification_friends'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_chat', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_chat', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='notification_messages',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('time_sent', models.DateTimeField(default=django.utils.timezone.now)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.chat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
