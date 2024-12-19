from typing import List

from django.db.models import Prefetch
from django.http import HttpRequest
from ninja import NinjaAPI

from .models import Specialist, Service

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
