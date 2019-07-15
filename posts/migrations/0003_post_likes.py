# Generated by Django 2.2.3 on 2019-07-13 10:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_auto_20190713_0442'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, default=1, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]