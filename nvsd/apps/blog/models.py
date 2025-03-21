from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class Category(models.Model):
    name_uk = models.CharField(max_length=128, verbose_name=_('Назва категорії (Укр.)'))
    name_ru = models.CharField(max_length=128, verbose_name=_('Назва категорії (Рос.)'))

    class Meta:
        verbose_name = _('Категорія')
        verbose_name_plural = _('Категорії')

    def __str__(self):
        return f"{self.name_uk} / {self.name_ru}"


class Post(models.Model):
    title_uk = models.CharField(max_length=512, verbose_name=_("Заголовок (Укр.)"))
    title_ru = models.CharField(max_length=512, verbose_name=_("Заголовок (Рос.)"))
    description_uk = RichTextField(verbose_name=_('Опис статті (Укр.)'))
    description_ru = RichTextField(verbose_name=_('Опис статті (Рос.)'))
    published_at = models.DateTimeField(default=datetime.now(), verbose_name=_("Дата публікації (автоматично - сьогодні)"))
    photo_url = models.CharField(max_length=128, verbose_name=_("Головна картинка"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Категорія"))

    class Meta:
        verbose_name = _('Стаття')
        verbose_name_plural = _('Стаття')

    def clean(self):
        """Очищуємо buy_link та photo_url від зайвого HTML"""
        self.photo_url = strip_tags(self.photo_url).strip()

    def save(self, *args, **kwargs):
        """Перед збереженням очищаємо поля"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title_uk} / {self.title_ru}"
    pass