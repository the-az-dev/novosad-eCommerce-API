import datetime
from time import timezone
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, response
from django.core.paginator import Paginator

from .models import Product, SubCategoryFilter, FilterValue, SubCategory, Category, ProductFilterValue, ProductComments


def get_filters(request):
    subcategory_id = request.GET.get("id")
    locale = request.GET.get("locale", "uk")
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 1000))

    filters = None
    if subcategory_id == None:
        filters = SubCategoryFilter.objects.all()
    else:
        filters = SubCategoryFilter.objects.filter(
            subcategory_id=subcategory_id)

    response_data = []
    for filter in filters:
        values = list(FilterValue.objects.filter(
            filter=filter).values_list(f"value_{locale}", flat=True))

        response_data.append({
            "name": getattr(filter, f"name_{locale}"),
            "type": filter.type,
            "values": values if filter.type != "number" or filter.type != "number_range" else []
        })

    paginator = Paginator(response_data, per_page)
    page_obj = paginator.get_page(page)

    return JsonResponse({
        "status": 200 if response_data != [] else 404,
        "data": response_data,
        "request_date": datetime.datetime.now(),
        "pages": {
            "current": page_obj.number,
            "pages_amount": paginator.num_pages,
            "per_page": per_page
        }
    })
    

def get_category(request):
    category_id = request.GET.get("id")
    locale = request.GET.get("locale", "uk")
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 1000))

    if category_id is None:
        categorys = Category.objects.all()
    else:
        categorys = Category.objects.filter(id=category_id)

    response_data = []
    for category in categorys:
        subcategories = SubCategory.objects.filter(category=category)
        subcategory_data = [
            {
                "id": sub.id,
                "name": getattr(sub, f"name_{locale}")
            }
            for sub in subcategories
        ]

        response_data.append({
            "id": category.id,
            "name": getattr(category, f"name_{locale}"),
            "photo_url": category.photo_url,
            "subcategory": subcategory_data
        })

    paginator = Paginator(response_data, per_page)
    page_obj = paginator.get_page(page)

    return JsonResponse({
        "status": 200 if response_data else 404,
        "data": response_data,
        "request_date": datetime.datetime.now(),
        "pages": {
            "current": page_obj.number,
            "pages_amount": paginator.num_pages,
            "per_page": per_page
        }
    })


from django.db.models import Q

def get_products(request):
    product_name = request.GET.get("name")
    product_id = request.GET.get("id")
    locale = request.GET.get("locale", "uk")
    category = request.GET.get("category")
    subcategory_id = int(request.GET.get("subcategory_id", 0)) or None
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 20))
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")

    products = Product.objects.all()

    if product_id:
        products = products.filter(id=product_id)

    if category:
        if locale == "uk":
            products = products.filter(subcategory__category__name_uk=category)
        else:
            products = products.filter(subcategory__category__name_ru=category)

    if product_name:
        if locale == "uk":
            products = products.filter(name_uk__icontains=product_name)
        else:
            products = products.filter(name_ru__icontains=product_name)

    if subcategory_id:
        products = products.filter(subcategory__id=subcategory_id)

    print(f"🔍 subcategory_id: {subcategory_id}")

    # Фільтр по ціні
    if price_min:
        products = products.filter(price__gte=float(price_min))
    if price_max:
        products = products.filter(price__lte=float(price_max))

    # Обробка фільтрів по характеристиках
    filter_keys = [key for key in request.GET.keys() if key.startswith("filter_")]
    for key in filter_keys:
        filter_name = key.replace("filter_", "")
        filter_value = request.GET.get(key)

        if locale == "uk":
            products = products.filter(
                filter_values__filter__name_uk=filter_name,
                filter_values__value_uk=filter_value
            )
        else:
            products = products.filter(
                filter_values__filter__name_ru=filter_name,
                filter_values__value_ru=filter_value
            )

    # Унікальні товари (бо при .filter(filter_values__...) може бути дублікати)
    products = products.distinct()

    response_data = []
    for product in products:
        values = {
            getattr(pfv.filter, f"name_{locale}"): getattr(pfv, f"value_{locale}")
            for pfv in product.filter_values.select_related("filter")
        }

        category_data = {
            "id": product.subcategory.id,
            "name": getattr(product.subcategory, f"name_{locale}", "Невідомо"),
        } if product.subcategory else None

        comments_data = [
            {
                "username": comment.username,
                "rating": comment.rating,
                "date": comment.date,
                "comment": comment.comment
            }
            for comment in ProductComments.objects.filter(product=product)
        ]

        response_data.append({
            "id": product.id,
            "name": getattr(product, f"name_{locale}"),
            "description": getattr(product, f"description_{locale}"),
            "price": float(product.price),
            "minimal_order": product.minimal_order,
            "delivery_at": product.delivery_at,
            "buy_link": product.buy_link,
            "photo_url": product.photo_url,
            "category": category_data,
            "attributes": values,
            "comments": comments_data
        })

    paginator = Paginator(response_data, per_page)
    page_obj = paginator.get_page(page)

    return JsonResponse({
        "status": 200 if response_data else 404,
        "data": response_data if response_data else "No data found!",
        "request_date": datetime.datetime.now(),
        "pages": {
            "current": page_obj.number,
            "pages_amount": paginator.num_pages,
            "per_page": per_page
        }
    })
