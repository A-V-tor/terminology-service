# Generated by Django 4.1 on 2024-09-11 13:10

import datetime

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='HandBook',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'uniq_code',
                    models.CharField(
                        max_length=100, unique=True, verbose_name='Код'
                    ),
                ),
                (
                    'title',
                    models.TextField(
                        max_length=300, verbose_name='Наименование'
                    ),
                ),
                ('description', models.TextField(verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='VersionHandBook',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'version',
                    models.CharField(max_length=50, verbose_name='Версия'),
                ),
                (
                    'version_start_date',
                    models.DateField(
                        default=datetime.datetime.now,
                        verbose_name='Дата начала действия',
                    ),
                ),
                (
                    'handbook',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='api_v1.handbook',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='HandBookElement',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'uniq_code',
                    models.CharField(max_length=100, verbose_name='Код'),
                ),
                (
                    'value',
                    models.TextField(max_length=300, verbose_name='значение'),
                ),
                (
                    'version_hand_book',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='api_v1.versionhandbook',
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name='versionhandbook',
            constraint=models.UniqueConstraint(
                fields=('handbook', 'version'), name='unique_handbook_version'
            ),
        ),
        migrations.AddConstraint(
            model_name='versionhandbook',
            constraint=models.UniqueConstraint(
                fields=('handbook', 'version_start_date'),
                name='unique_version_start_date_per_handbook',
            ),
        ),
        migrations.AddConstraint(
            model_name='handbookelement',
            constraint=models.UniqueConstraint(
                fields=('version_hand_book', 'uniq_code'),
                name='unique_version_hand_book_uniq_code',
            ),
        ),
    ]
