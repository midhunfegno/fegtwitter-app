# Generated by Django 3.2.13 on 2022-05-17 08:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fegtwitterapp', '0006_alter_usertweet_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='_fegtwitterapp_user_followers_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
