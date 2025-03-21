"""
URL configuration for nvsd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

from nvsd.apps import blog

admin.site.index_title = _('Novosad Admin')
admin.site.site_header = _('Novosad Site Administration')
admin.site.site_title = _('Novosad Site Content Management')

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('blog/', include('blog.urls')),
    
    # Do not touch this line of code cuz its basic config
    prefix_default_language=False
)
