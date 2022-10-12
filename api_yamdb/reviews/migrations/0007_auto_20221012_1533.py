# Generated by Django 2.2.16 on 2022-10-12 12:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0006_auto_20221012_1326'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_title_author',
        ),
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('title', 'author')},
        ),
    ]