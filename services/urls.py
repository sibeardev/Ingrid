from django.urls import path

from services import views
from services.api import api

urlpatterns = [
    path("", views.index, name="main_page"),
    path("manager/", views.manager_page, name="manager_page"),
    path("notes/", views.notes, name="notes"),
    path("service/", views.service, name="service"),
    path("service-finally/", views.service_finally, name="service_finally"),
    path("api/", api.urls),
    path("index/", views.index, name="index"),
    path("auth/", views.auth, name="auth"),
]
