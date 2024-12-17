from django.contrib import admin

from .models import Client
from .models import Salon
from .models import Service
from .models import Specialist
from .models import Order
from .models import SpecialistWorkDayInSalon
from .models import Appointment


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


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
