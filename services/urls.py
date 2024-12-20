from django.urls import path

from services import views

urlpatterns = [
    path("", views.index, name="main_page"),
    path("manager/", views.manager_page, name="manager_page"),
    path("notes/", views.notes, name="notes"),
    path("service/", views.service, name="service"),
    path("service-finally/", views.service_finally, name="service_finally"),
    path('index/', views.index, name='index'),
]
