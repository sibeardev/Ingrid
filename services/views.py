from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Salon, Specialist, Service, SpecialistWorkDayInSalon
from .forms import ConsultationForm


def index(request: HttpRequest) -> HttpResponse:
    salons = Salon.objects.all()
    specialists = Specialist.objects.all()
    services = Service.objects.all()
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['name'] = post_data.get('fname')
        post_data['phone_number'] = post_data.get('tel')
        post_data['question'] = post_data.get('contactsTextarea')

        form = ConsultationForm(post_data)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно создана")
            return render(request, "index.html", {
                "salons": salons,
                "specialists": specialists,
                "services": services,
                "form": ConsultationForm(),
            })

    context = {
        "salons": salons,
        "specialists": specialists,
        "services": services,
        "form": ConsultationForm()
    }
    return render(request, "index.html", context)


def manager_page(request: HttpRequest) -> HttpResponse:
    return render(request, "admin.html")


def notes(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        print("POST-запрос получен")  # Лог для проверки
        return redirect('notes')  # Перенаправление
    print("GET-запрос получен")
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
