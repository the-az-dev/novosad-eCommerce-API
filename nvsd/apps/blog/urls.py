from django.urls import path

from . import views

urlpatterns = [

    # GET REQUESTS
    path('category/get/', views.get_categories, name='get_categories'),
    path('category/get/<int:id>/', views.get_category, name='get_category'),
    path('post/get/', views.get_posts, name='get_posts'),
    path('post/get/<int:id>/', views.get_post, name='get_post'),
    # POST REQUESTS

    # PUT REQUESTS

    # DELETE REQUESTS

]
