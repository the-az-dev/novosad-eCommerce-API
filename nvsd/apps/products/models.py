from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class Category(models.Model):
    name_uk = models.CharField(max_length=128, verbose_name=_('Назва категорії (Укр.)'))
    name_ru = models.CharField(max_length=128, verbose_name=_('Назва категорії (рос.)'))
    photo_url = models.TextField(verbose_name=_('Фото категорії'))

    class Meta:
        verbose_name = _('Категорія')
        verbose_name_plural = _('Категорії')

    def __str__(self):
        return f"{self.name_uk} / {self.name_ru}"

class SubCategory(models.Model):
    name_uk = models.CharField(max_length=256, verbose_name=_('Назва категорії (Укр.)'))
    name_ru = models.CharField(max_length=256, verbose_name=_('Назва категорії (рос.)'))
    photo_url = models.TextField(verbose_name=_('Фото підкатегорії'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        verbose_name = _('Підкатегорія')
        verbose_name_plural = _('Підкатегорії')

    def __str__(self):
        return f"{self.name_uk} / {self.name_ru}"

class SubCategoryFilter(models.Model):
    TYPE_CHOICES = [
        ('text', _('Текст')),
        ('number', _('Число')),
        ('select', _('Варіант вибору')),
        ('boolean', _("Так/ні"))
    ]

    name_uk = models.CharField(max_length=256, verbose_name=_('Назва характеристики (Укр.)'))
    name_ru = models.CharField(max_length=256, verbose_name=_('Назва характеристики (рос.)'))
    type = models.CharField(choices=TYPE_CHOICES, max_length=128, verbose_name=_('Тип характеристики'))
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='filters')

    class Meta:
        verbose_name = _('Характеристика підкатегорії')
        verbose_name_plural = _('Характеристики підкатегорії')

    def __str__(self):
        return f"{self.name_uk} / {self.name_ru}"
    
    def get(key):
        pass

class FilterValue(models.Model):
    filter = models.ForeignKey(SubCategoryFilter, on_delete=models.CASCADE, related_name='values')
    value_uk = models.CharField(max_length=256, verbose_name=_('Значення характеристики (укр.)'))
    value_ru = models.CharField(max_length=256, verbose_name=_('Значення характеристики (рос.)'))

    class Meta:
        verbose_name = _('Значення характеристики')
        verbose_name_plural = _('Значення характеристик')

    def __str__(self):
        return f"{self.filter.name_uk}: {self.value_uk}"

class Product(models.Model):
    name_uk = models.CharField(max_length=256, verbose_name=_('Назва товару (Укр.)'))
    name_ru = models.CharField(max_length=256, verbose_name=_('Назва товару (рос.)'))
    description_uk = RichTextField(verbose_name=_('Опис товару (Укр.)'))
    description_ru = RichTextField(verbose_name=_('Опис товару (рос.)'))
    price = models.FloatField(verbose_name=_('Ціна'))
    minimal_order = models.IntegerField(verbose_name=_('Мінімальна к-сть на ціну'))
    delivery_at = models.DateField(verbose_name=_('Дата відправки'))
    buy_link = models.TextField(verbose_name=_('Посилання на покупку'))
    photo_url = models.TextField(verbose_name=_('Фото товару'))
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')

    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товари')

    def __str__(self):
        return f"{self.name_uk} / {self.name_ru}"
    
    def clean(self):
        """Очищуємо buy_link та photo_url від зайвого HTML"""
        self.buy_link = strip_tags(self.buy_link).strip()
        self.photo_url = strip_tags(self.photo_url).strip()

    def save(self, *args, **kwargs):
        """Перед збереженням очищаємо поля"""
        self.clean()
        super().save(*args, **kwargs)

class ProductFilterValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='filter_values')
    filter = models.ForeignKey(SubCategoryFilter, on_delete=models.CASCADE, related_name='product_values')
    value_uk = models.CharField(max_length=256, verbose_name=_('Значення характеристики товару (uk)'))
    value_ru = models.CharField(max_length=256, verbose_name=_('Значення характеристики товару (ru)'))

    class Meta:
        verbose_name = _('Характеристика товару')
        verbose_name_plural = _('Характеристики товару')

    def __str__(self):
        return f"{self.product.name_uk} - {self.filter.name_uk}: {self.value_uk}"
    
class ProductComments(models.Model):
    username=models.CharField(max_length=256, verbose_name=_("Імʼя клієнта"))
    rating=models.IntegerField(default=0, verbose_name=_("Оцінка"))
    date=models.DateTimeField(default=datetime.now(), verbose_name=_("Дата публікації"))
    comment=models.TextField(verbose_name=_("Коментар"))
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')