# Generated by Django 2.2.19 on 2022-10-14 00:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0013_auto_20221013_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.TextField(db_index=True, max_length=256, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.TextField(db_index=True, max_length=256, verbose_name='Название жанра'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='title',
            field=models.ManyToManyField(db_index=True, related_name='genre', to='reviews.Title'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.TextField(db_index=True, max_length=256, verbose_name='Название произедения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(2022), django.core.validators.MinValueValidator(-4000)]),
        ),
    ]
