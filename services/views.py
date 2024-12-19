from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Salon, Specialist, Service


def index(request: HttpRequest) -> HttpResponse:
    salons = Salon.objects.all()
    specialists = Specialist.objects.all()
    services = Service.objects.all()
    context = {"salons": salons, "specialists": specialists, "services": services}

    return render(request, "index.html", context)


def manager_page(request: HttpRequest) -> HttpResponse:
    return render(request, "admin.html")


def notes(request: HttpRequest) -> HttpResponse:
    return render(request, "notes.html")


def service(request: HttpRequest) -> HttpResponse:
    salons = Salon.objects.all()
    specialists = Specialist.objects.all()
    services = Service.objects.all()
    context = {"salons": salons, "specialists": specialists, "services": services}

    return render(request, "service.html", context)


def service_finally(request: HttpRequest) -> HttpResponse:
    return render(request, "serviceFinally.html")
