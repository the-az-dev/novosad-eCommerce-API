import datetime as datetime
from django.http import HttpResponse, JsonResponse, response
from django.core.paginator import Paginator
from .models import Category, Post

def get_posts(request):
    locale = request.GET.get("locale", "uk")
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 1000))

    posts = Post.objects.all()
    response_data = []
    for post in posts:
        category = {
            "id": post.category.id,
            "name": getattr(post.category, f"name_{locale}"),
        }
        response_data.append(
            {
                "id": post.id,
                "title": getattr(post, f"title_{locale}"),
                "description": getattr(post, f"description_{locale}"),
                "published_at": post.published_at,
                "photo_url": post.photo_url,
                "category": category,
            }
        )

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

def get_post(request, id):
    locale = request.GET.get("locale", "uk")
    post = Post.objects.get(id=id)
    category = {
        "id": post.category.id,
        "name": getattr(post.category, f"name_{locale}"),
    }
    response_data=[{
        "id": post.id,
        "title": getattr(post, f"title_{locale}"),
        "description": getattr(post, f"description_{locale}"),
        "published_at": post.published_at,
        "photo_url": post.photo_url,
        "category": category,
    }]
    return JsonResponse({
        "status": 200 if response_data != [] else 404,
        "data": response_data,
        "request_date": datetime.datetime.now(),
    })

def get_categories(request):
    locale = request.GET.get("locale", "uk")
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 1000))

    categories = Category.objects.all()
    response_data = []
    for category in categories:
        response_data.append({
            "id": category.id,
            "title": getattr(category, f"name_{locale}"),
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

def get_category(request, id):
    locale = request.GET.get("locale", "uk")
    category = Category.objects.get(id=id)
    response_data = [{
        "id": category.id,
        "name": getattr(category, f"name_{locale}"),
    }]

    return JsonResponse({
        "status": 200 if response_data != [] else 404,
        "data": response_data,
        "request_date": datetime.datetime.now(),
    })