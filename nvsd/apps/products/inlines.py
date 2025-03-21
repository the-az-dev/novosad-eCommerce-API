from django.contrib import admin
from .models import Category, SubCategory, SubCategoryFilter, FilterValue, Product, ProductFilterValue
from django.forms.models import BaseInlineFormSet
from django.forms import inlineformset_factory
from django.urls import path
from django.utils.safestring import mark_safe
import nested_admin

class FilterValueInline(nested_admin.NestedStackedInline):
    model = FilterValue
    extra = 1
    
class SubCategoryFilterInline(nested_admin.NestedStackedInline):
    model=SubCategoryFilter
    extra=1
    inlines = [FilterValueInline]

class SubCategoryInline(nested_admin.NestedStackedInline):
    model=SubCategory
    extra=1
    
class ProductInline(admin.TabularInline):
    model=Product
    extra=1
    
class ProductFilterValueInline(admin.TabularInline):
    model = ProductFilterValue
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Фільтруємо фільтри тільки по вибраній підкатегорії"""
        if db_field.name == "filter":
            obj_id = request.resolver_match.kwargs.get("object_id")
            if obj_id:
                product = Product.objects.get(pk=obj_id)
                kwargs["queryset"] = SubCategoryFilter.objects.filter(subcategory=product.subcategory)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """Якщо фільтр має тип 'select', вибираємо можливі значення"""
        if db_field.name == "value_uk" or db_field.name == "value_ru":
            obj_id = request.resolver_match.kwargs.get("object_id")
            if obj_id:
                product = Product.objects.get(pk=obj_id)
                filters = SubCategoryFilter.objects.filter(subcategory=product.subcategory, type="select")
                filter_values = FilterValue.objects.filter(filter__in=filters)
                kwargs["choices"] = [(fv.value_uk, fv.value_uk) for fv in filter_values]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

