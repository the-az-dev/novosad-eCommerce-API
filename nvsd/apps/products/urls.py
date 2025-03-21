from django.urls import path

from . import views 

urlpatterns = [
    
    # GET REQUESTS
    path('filters/get', views.get_filters, name='get_filters'),
    path('category/get', views.get_category, name='get_category'),
    path('get', views.get_products, name='get_products'),
    
    # POST REQUESTS
    
    
    # PUT REQUESTS
    
    
    # DELETE REQUESTS
    
    
]
