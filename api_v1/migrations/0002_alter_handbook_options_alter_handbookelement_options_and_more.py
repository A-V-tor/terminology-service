# Generated by Django 4.1 on 2024-09-11 15:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='handbook',
            options={
                'verbose_name': 'Справочник',
                'verbose_name_plural': 'Справочники',
            },
        ),
        migrations.AlterModelOptions(
            name='handbookelement',
            options={
                'verbose_name': 'Элемент справочника',
                'verbose_name_plural': 'Элементы справочников',
            },
        ),
        migrations.AlterModelOptions(
            name='versionhandbook',
            options={
                'verbose_name': 'Версия справочник',
                'verbose_name_plural': 'Версия справочников',
            },
        ),
        migrations.AlterField(
            model_name='handbookelement',
            name='version_hand_book',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='elements',
                to='api_v1.versionhandbook',
                verbose_name='Версия справочника',
            ),
        ),
        migrations.AlterField(
            model_name='versionhandbook',
            name='handbook',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='versions',
                to='api_v1.handbook',
                verbose_name='Справочник',
            ),
        ),
    ]
