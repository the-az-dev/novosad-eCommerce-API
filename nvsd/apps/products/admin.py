from django.contrib import admin
from .models import Category, SubCategory, SubCategoryFilter, FilterValue, Product, ProductFilterValue
from .inlines import *
from django.http import JsonResponse
from django.urls import path
import nested_admin
from ckeditor.widgets import CKEditorWidget
from django.db import models
from django import forms

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_uk', 'name_ru')
    search_fields = ('name_uk', 'name_ru',)
    inlines=[SubCategoryInline]

@admin.register(SubCategoryFilter)
class SubCategoryFilterAdmin(admin.ModelAdmin):
    list_display = ('name_uk', 'name_ru', 'type', 'subcategory')
    search_fields = ('name_uk', 'name_ru')
    list_filter = ('subcategory',)
    inlines = [FilterValueInline]

@admin.register(SubCategory)
class SubCategoryAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name_uk', 'name_ru', 'category',)
    search_fields = ('name_uk', 'name_ru')
    list_filter = ('category',)
    inlines = [SubCategoryFilterInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }
    
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "buy_link": forms.Textarea(),
            "photo_url": forms.Textarea(),
        }
    
    list_display = ('name_uk', 'name_ru', 'description_uk', 'description_ru', 'price', 'subcategory')
    search_fields = ('name_uk', 'name_ru',)
    list_filter = ('subcategory',)
    inlines = [ProductFilterValueInline]

@admin.register(ProductFilterValue)
class ProductFilterValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'filter', 'value_uk', 'value_ru')
    search_fields = ('product__name', 'filter__name', 'value_uk', 'value_ru')
    list_filter = ('filter',)
