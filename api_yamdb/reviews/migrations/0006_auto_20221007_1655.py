# Generated by Django 2.2.16 on 2022-10-07 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20221007_1651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='review_id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='text',
        ),
        migrations.RemoveField(
            model_name='review',
            name='author',
        ),
        migrations.RemoveField(
            model_name='review',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='review',
            name='score',
        ),
        migrations.RemoveField(
            model_name='review',
            name='text',
        ),
        migrations.RemoveField(
            model_name='review',
            name='title_id',
        ),
    ]
