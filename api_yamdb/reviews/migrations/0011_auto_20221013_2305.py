# Generated by Django 2.2.19 on 2022-10-13 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_auto_20221013_2258'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': ('Категория',), 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': ('Жанр',), 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'verbose_name': ('Произведение',), 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.TextField(max_length=256, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.TextField(max_length=256, verbose_name='Название жанра'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.TextField(max_length=256, verbose_name='Название произедения'),
        ),
    ]
