from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Salon, Specialist, Service, SpecialistWorkDayInSalon


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
    """Отображает выбранный салон, услугу, мастера, дату и время для подтверждения записи"""

    specialist_id = request.GET.get("specialist_id")
    service_id = request.GET.get("service_id")
    selected_date = datetime.strptime(request.GET.get("date"), "%Y-%m-%d").date()
    selected_time = datetime.strptime(request.GET.get("time"), "%H:%M").time()

    workday = (
        SpecialistWorkDayInSalon.objects.select_related("salon", "specialist")
        .prefetch_related("specialist__services")
        .filter(
            specialist_id=specialist_id,
            workday=selected_date,
        )
        .first()
    )

    service = (
        Service.objects.get(id=service_id)
        if service_id
        else workday.specialist.services.first()
    )

    context = {
        "date": selected_date,
        "time": selected_time,
        "service": service,
        "salon": workday.salon,
        "specialist": workday.specialist,
    }

    return render(request, "serviceFinally.html", context)
