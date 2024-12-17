from django.contrib import admin
from django.db.models import Count

from .models import Client
from .models import Salon
from .models import Service
from .models import Specialist
from .models import Order
from .models import SpecialistWorkDayInSalon
from .models import Appointment


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "full_name",)

    def total_clients_count(self, obj):
        return Client.objects.count()

    total_clients_count.short_description = "Общее количество клиентов"


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(SpecialistWorkDayInSalon)
class SpecialistWorkDayInSalonAdmin(admin.ModelAdmin):
    pass


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass
