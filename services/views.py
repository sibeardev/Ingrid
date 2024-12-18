from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Salon, Specialist


def index(request: HttpRequest) -> HttpResponse:
    salons = Salon.objects.all()
    specialists = Specialist.objects.all()
    context = {"salons": salons, "specialists": specialists}

    return render(request, "index.html", context)


def manager_page(request: HttpRequest) -> HttpResponse:
    return render(request, "admin.html")


def notes(request: HttpRequest) -> HttpResponse:
    return render(request, "notes.html")


def service(request: HttpRequest) -> HttpResponse:
    return render(request, "service.html")


def service_finally(request: HttpRequest) -> HttpResponse:
    return render(request, "serviceFinally.html")
