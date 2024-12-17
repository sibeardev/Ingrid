from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


def manager_page(request: HttpRequest) -> HttpResponse:
    return render(request, "admin.html")


def notes(request: HttpRequest) -> HttpResponse:
    return render(request, "notes.html")


def service(request: HttpRequest) -> HttpResponse:
    return render(request, "service.html")


def service_finally(request: HttpRequest) -> HttpResponse:
    return render(request, "serviceFinally.html")
