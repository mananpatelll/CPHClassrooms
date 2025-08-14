"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from classrooms.views import buildings_index, classroom_list_by_building, classroom_detail
from django.http import HttpResponse

urlpatterns = [
   # Home now shows buildings:
    path('', buildings_index, name='home'),

    # Buildings:
    path('buildings/', buildings_index, name='buildings_index'),
    path('buildings/<slug:building_slug>/', classroom_list_by_building, name='building_classrooms'),

    # Classrooms (detail stays the same):
    path('classrooms/<int:pk>/', classroom_detail, name='classroom_detail'),
    # admin left out on purpose for PoC
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)