"""coronavirus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from modelling.views import get_country_state, getTimeSeriesGraph
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', get_country_state, name='home'),
    path('admin/', admin.site.urls),
    path('ajax/get_country/', getTimeSeriesGraph, name='get_graph'),
    path('ajax/getcountry_state/', getTimeSeriesGraph, name='get_graph'),
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

