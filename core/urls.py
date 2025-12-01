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
from classrooms.views import buildings_index, classroom_list_by_building, classroom_detail, classroom_detail_pk
from django.http import HttpResponse


from classrooms import views as cviews


urlpatterns = [
   # Home now shows buildings:
    path("", cviews.buildings_index, name="home"),
    
    path("buildings/", cviews.buildings_index, name="buildings_index"),     # Buildings:

    path("buildings/<slug:slug>/", cviews.classroom_list_by_building, name="classroom_list_by_building"),
    path("buildings/<slug:slug>/<str:room_number>/", cviews.classroom_detail, name="classroom_detail"),
    path("classrooms/<int:pk>/", cviews.classroom_detail_pk, name="classroom_detail_pk"), 
    
    path(settings.ADMIN_URL, admin.site.urls),
    path("healthz/", lambda r: HttpResponse("ok"), name="healthz")

]

if settings.DEBUG and settings.STORAGE_BACKEND == "local":
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)