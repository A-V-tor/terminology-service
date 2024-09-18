from datetime import datetime

from django.db import models


class HandBook(models.Model):
    uniq_code = models.CharField(
        max_length=100, unique=True, null=False, verbose_name='Код'
    )
    title = models.TextField(
        max_length=300, null=False, verbose_name='Наименование'
    )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

    def __str__(self):
        return f'{self.title} - {self.uniq_code}'


class VersionHandBook(models.Model):
    version = models.CharField(
        max_length=50, null=False, verbose_name='Версия'
    )
    version_start_date = models.DateField(
        default=datetime.now, verbose_name='Дата начала действия'
    )

    handbook = models.ForeignKey(
        'HandBook',
        on_delete=models.CASCADE,
        null=False,
        related_name='versions',
        verbose_name='Справочник',
    )

    class Meta:
        verbose_name = 'Версия справочник'
        verbose_name_plural = 'Версия справочников'
        constraints = [
            models.UniqueConstraint(
                fields=['handbook', 'version'], name='unique_handbook_version'
            ),
            models.UniqueConstraint(
                fields=['handbook', 'version_start_date'],
                name='unique_version_start_date_per_handbook',
            ),
        ]

    def __str__(self):
        return f'{self.version} - {self.handbook.title}'


class HandBookElement(models.Model):
    version_hand_book = models.ForeignKey(
        'VersionHandBook',
        on_delete=models.CASCADE,
        null=False,
        related_name='elements',
        verbose_name='Версия справочника',
    )
    uniq_code = models.CharField(
        max_length=100, null=False, verbose_name='Код'
    )
    value = models.TextField(
        max_length=300, null=False, verbose_name='значение'
    )

    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочников'
        constraints = [
            models.UniqueConstraint(
                fields=['version_hand_book', 'uniq_code'],
                name='unique_version_hand_book_uniq_code',
            )
        ]

    def __str__(self):
        return f'{self.uniq_code}'
