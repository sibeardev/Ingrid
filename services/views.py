from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import ConsultationForm
from .models import (
    Salon,
    Specialist,
    Service,
    ServiceType,
    SpecialistWorkDayInSalon,
    CustomUser,
    Appointment,
    Client,
)


def index(request: HttpRequest) -> HttpResponse:
    salons = Salon.objects.all()
    specialists = Specialist.objects.all()
    services = Service.objects.all()
    if request.method == "POST":
        post_data = request.POST.copy()
        post_data["name"] = post_data.get("fname")
        post_data["phone_number"] = post_data.get("tel")
        post_data["question"] = post_data.get("contactsTextarea")

        form = ConsultationForm(post_data)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно создана")
            return render(
                request,
                "index.html",
                {
                    "salons": salons,
                    "specialists": specialists,
                    "services": services,
                    "form": ConsultationForm(),
                },
            )

    context = {
        "salons": salons,
        "specialists": specialists,
        "services": services,
        "form": ConsultationForm(),
    }
    return render(request, "index.html", context)


def manager_page(request: HttpRequest) -> HttpResponse:
    return render(request, "admin.html")


def auth(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        phone_number = request.POST.get("tel")
        # TODO: Добавить валидацию номера
        user, created = CustomUser.objects.get_or_create(
            phone_number=phone_number, defaults={"username": phone_number}
        )
        if created:
            user.save()
        login(request, user)

        return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        return HttpResponse("Метод не поддерживается", status=405)


def notes(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        print("POST-запрос получен")  # Лог для проверки
        return redirect("notes")  # Перенаправление
    print("GET-запрос получен")
    return render(request, "notes.html")


def service(request: HttpRequest) -> HttpResponse:
    # Получаем все типы услуг и связанные с ними услуги
    service_types = ServiceType.objects.all().prefetch_related("services")

    # Получаем все салоны
    salons = Salon.objects.all()

    # Получаем всех специалистов
    specialists = Specialist.objects.all()

    # Формируем данные для шаблона
    service_types_data = []
    for service_type in service_types:
        services_data = [
            {
                "id": service.id,
                "title": service.title,
                "price": service.price,
            }
            for service in service_type.services.all()
        ]
        service_types_data.append(
            {
                "id": service_type.id,
                "title": service_type.title,
                "services": services_data,
            }
        )

    # Передаем данные в контекст шаблона
    context = {
        "salons": salons,
        "specialists": specialists,
        "service_types": service_types_data,
    }

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


def confirm_appointment(request: HttpRequest) -> HttpResponse:
    """Создание записи на услугу"""
    if request.method == "POST":
        specialist_id = request.POST.get("specialist_id")
        time = request.POST.get("time")
        date = datetime.fromtimestamp(int(request.POST.get("date"))).date()
        service_id = request.POST.get("service_id")
        phone_number = request.POST.get("tel")
        full_name = request.POST.get("fname")

        client, created = Client.objects.update_or_create(
            phone_number=phone_number, defaults={"full_name": full_name}
        )
        if created:
            client.save()

        workday = (
            SpecialistWorkDayInSalon.objects.select_related("salon", "specialist")
            .prefetch_related("specialist__services")
            .filter(
                specialist_id=specialist_id,
                workday=date,
            )
            .first()
        )

        service = (
            Service.objects.get(id=service_id)
            if service_id
            else workday.specialist.services.first()
        )

        appointment, created = Appointment.objects.get_or_create(
            salon=workday.salon,
            specialist=workday.specialist,
            service=service,
            date=date,
            start_at=time,
            client=client,
        )
        if created:
            appointment.save()

        return redirect("notes")
    else:
        return HttpResponse("Метод не поддерживается", status=405)
