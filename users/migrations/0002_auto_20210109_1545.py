# Generated by Django 3.1.1 on 2021-01-09 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movieslistuser',
            old_name='url_img',
            new_name='url_image',
        ),
        migrations.RenameField(
            model_name='movieslistuser',
            old_name='average',
            new_name='vote_average',
        ),
    ]
