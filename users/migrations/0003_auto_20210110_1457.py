# Generated by Django 3.1.1 on 2021-01-10 14:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_auto_20210109_1545'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='movieslistuser',
            unique_together={('user', 'title')},
        ),
    ]