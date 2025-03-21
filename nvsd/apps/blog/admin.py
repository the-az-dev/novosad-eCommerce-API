from django.contrib import admin
from .models import Category, Post
from ckeditor.widgets import CKEditorWidget
from django.db import models
from django import forms


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_uk', 'name_ru')
    search_fields = ('name_uk', 'name_ru',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }

    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            "photo_url": forms.Textarea(),
        }

    list_display = ("title_uk", "title_ru", "description_uk", "description_ru", "category", "published_at", "photo_url")
    search_fields = ("title_uk", "title_ru", "category__name_uk", "category__name_ru", "published_at",)