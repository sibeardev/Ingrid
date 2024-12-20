from datetime import datetime, timedelta, time
from typing import List

from django.db.models import Prefetch
from django.http import HttpRequest
from ninja import NinjaAPI

from .models import Specialist, Service, SpecialistWorkDayInSalon

api = NinjaAPI()


@api.get("/services/", response=List[dict])
def get_services_and_specialists(request: HttpRequest, salon_id: int) -> List[dict]:
    """
    Получить услуги и специалистов, связанных с салоном.
    """

    specialists = Specialist.objects.filter(salon_id=salon_id).prefetch_related(
        Prefetch("services")
    )

    services = Service.objects.filter(specialists__salon_id=salon_id).distinct()

    specialists_data = [
        {
            "id": specialist.id,
            "full_name": specialist.full_name,
            "position": specialist.position,
            "image_url": specialist.image.url if specialist.image else None,
        }
        for specialist in specialists
    ]

    services_data = [
        {
            "id": service.id,
            "title": service.title,
            "price": service.price,
        }
        for service in services
    ]

    return [{"specialists": specialists_data, "services": services_data}]


@api.get("/specialists/", response=List[dict])
def get_specialists_by_service(
    request: HttpRequest, service_id, salon_id: int = None
) -> List[dict]:
    """
    Получить специалистов, связанных с определённой услугой.
    Если передан salon_id, то фильтруем по этому салону.
    """
    specialists_queryset = Specialist.objects.filter(services__id=service_id)

    if salon_id:
        specialists_queryset = specialists_queryset.filter(salon__id=salon_id)

    specialists = [
        {
            "id": specialist.id,
            "full_name": specialist.full_name,
            "position": specialist.position,
            "image_url": specialist.image.url if specialist.image else None,
        }
        for specialist in specialists_queryset
    ]

    return [{"specialists": specialists}]


@api.get("/specialist_workday/", response=List[dict])
def get_workday_timeslots(request, specialist_id: int, selected_date: str):
    """
    Получить времени рабочего дня специалиста для выбранной даты.
    """

    try:
        workday_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
        workday = SpecialistWorkDayInSalon.objects.filter(
            specialist_id=specialist_id,
            workday=workday_date,
        ).first()
        timeslots = {"morning": [], "day": [], "evening": []}
        if workday:
            current_time = workday.start_at
            interval_minutes = 60  # TODO: интервал в настройки?
            while current_time < workday.end_at:
                if time(6, 0) < current_time < time(12, 0):
                    timeslots["morning"].append(current_time.strftime("%H:%M"))
                elif time(12, 0) < current_time < time(18, 0):
                    timeslots["day"].append(current_time.strftime("%H:%M"))
                elif time(18, 0) < current_time < time(23, 0):
                    timeslots["evening"].append(current_time.strftime("%H:%M"))
                current_time = (
                    datetime.combine(workday_date, current_time)
                    + timedelta(minutes=interval_minutes)
                ).time()

        return [{"timeslots": timeslots}]

    except Exception as e:
        return [{"error": str(e)}]
