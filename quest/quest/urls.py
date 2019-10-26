from django.contrib import admin
from django.urls import include
from django.urls import path
from grade.urls import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("grade.urls")),
    path("api/", include(router.urls)),
    ]
