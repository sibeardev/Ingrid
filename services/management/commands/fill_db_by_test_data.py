from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from services.models import Client, Salon, Service, Specialist, Order, ServiceType, SpecialistWorkDayInSalon, Appointment


class Command(BaseCommand):
    help = 'Заполнить базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            # Создание клиентов
            client_1 = Client.objects.create(full_name='Ричард', phone_number='+79004217012')
            client_2 = Client.objects.create(full_name='Егор', phone_number='+79004216012')
            client_3 = Client.objects.create(full_name='Александр', phone_number='+79004215012')
            client_4 = Client.objects.create(full_name='Николай', phone_number='+79004214012')
            client_5 = Client.objects.create(full_name='Виктория', phone_number='+79004213012')
            client_6 = Client.objects.create(full_name='Елизавета', phone_number='+79004212012')
            client_7 = Client.objects.create(full_name='Христина', phone_number='+79004211012')

            # Создание салонов
            with open('./static/img/salons/salon1.svg', 'rb') as f:
                salon_1 = Salon.objects.create(
                    title="BeautyCity Пушкинская",
                    address="ул. Пушкинская, д. 78А",
                    image=File(f)
                )
            with open('./static/img/salons/salon2.svg', 'rb') as f:
                salon_2 = Salon.objects.create(
                    title="BeautyCity Ленина",
                    address="ул. Ленина, д. 211",
                    image=File(f)
                )
            with open('./static/img/salons/salon3.svg', 'rb') as f:
                salon_3 = Salon.objects.create(
                    title="BeautyCity Красная",
                    address="ул. Красная, д. 10",
                    image=File(f)
                )
            # Создание типов услуг
            s_type_1 = ServiceType.objects.create(title='Парикмахерские услуги')
            s_type_2 = ServiceType.objects.create(title='Ногтевой сервис')
            s_type_3 = ServiceType.objects.create(title='Макияж')
            # Создание услуг
            with open('./static/img/services/service3.svg', 'rb') as f:
                service_1 = Service.objects.create(title="Укладка волос", s_type=s_type_1, price=1400.0, duration=180, image=File(f))
            with open('./static/img/services/service6.svg', 'rb') as f:
                service_2 = Service.objects.create(title="Окрашивание волос", s_type=s_type_1, price=5000.0, duration=180, image=File(f))

            with open('./static/img/services/service1.svg', 'rb') as f:
                service_3 = Service.objects.create(title="Дневной макияж", s_type=s_type_3, price=1400.0, duration=180, image=File(f))
            with open('./static/img/services/service4.svg', 'rb') as f:
                service_4 = Service.objects.create(title="Свадебный макияж", s_type=s_type_3, price=3000.0, duration=180, image=File(f))
            with open('./static/img/services/service1.svg', 'rb') as f:
                service_5 = Service.objects.create(title="Вечерний макияж", s_type=s_type_3, price=2000.0, duration=180, image=File(f))

            with open('./static/img/services/service2.svg', 'rb') as f:
                service_6 = Service.objects.create(title="Маникюр. Классический. Гель", s_type=s_type_2, price=2000.0, duration=180, image=File(f))
            with open('./static/img/services/service5.svg', 'rb') as f:
                service_7 = Service.objects.create(title="Педикюр", s_type=s_type_2, price=1000.0, duration=180, image=File(f))
            with open('./static/img/services/service2.svg', 'rb') as f:
                service_8 = Service.objects.create(title="Наращивание ногтей", s_type=s_type_2, price=1400.0, duration=180, image=File(f))

            # Создание специалистов
            with open('./static/img/masters/master1.svg', 'rb') as f:
                specialist_1 = Specialist.objects.create(full_name="Елизавета Лапина", position='Мастер маникюра', work_experience_years=3, work_experience_months=10, image=File(f))
            specialist_1.services.add(service_6)
            with open('./static/img/masters/master2.svg', 'rb') as f:
                specialist_2 = Specialist.objects.create(full_name="Анастасия Сергеевна", position='Парикмахер', work_experience_years=4, work_experience_months=9, image=File(f))
            specialist_2.services.add(service_1, service_2)
            with open('./static/img/masters/master3.svg', 'rb') as f:
                specialist_3 = Specialist.objects.create(full_name="Ева Колесова", position='Визажист', work_experience_years=1, work_experience_months=2, image=File(f))
            specialist_3.services.add(service_3, service_4, service_5)
            with open('./static/img/masters/master4.svg', 'rb') as f:
                specialist_4 = Specialist.objects.create(full_name="Мария Суворова", position='Стилист', work_experience_years=1, work_experience_months=1, image=File(f))
            specialist_4.services.add(service_2, service_3, service_4, service_5)
            with open('./static/img/masters/master5.svg', 'rb') as f:
                specialist_5 = Specialist.objects.create(full_name="Мария Максимова", position='Стилист', work_experience_years=3, work_experience_months=1, image=File(f))
            specialist_5.services.add(service_1, service_3, service_4, service_5)
            with open('./static/img/masters/master6.svg', 'rb') as f:
                specialist_6 = Specialist.objects.create(full_name="Майя Соболева", position='Визажист', work_experience_years=1, work_experience_months=1, image=File(f))
            specialist_6.services.add(service_3, service_4)

            # Создание рабочих дней
            workday_1 = SpecialistWorkDayInSalon.objects.create(
                workday="2024-12-28",
                salon=salon_1,
                specialist=specialist_1,
                start_at='08:00',
                end_at='18:00'
            )
            workday_2 = SpecialistWorkDayInSalon.objects.create(
                workday="2024-12-30",
                salon=salon_2,
                specialist=specialist_1,
                start_at='07:00',
                end_at='17:00'
            )
            workday_3 = SpecialistWorkDayInSalon.objects.create(
                workday="2025-01-03",
                salon=salon_3,
                specialist=specialist_1,
                start_at='08:00',
                end_at='18:00'
            )
            workday_4 = SpecialistWorkDayInSalon.objects.create(
                workday="2025-01-05",
                salon=salon_1,
                specialist=specialist_2,
                start_at='08:00',
                end_at='18:00'
            )
            workday_5 = SpecialistWorkDayInSalon.objects.create(
                workday="2025-01-12",
                salon=salon_2,
                specialist=specialist_2,
                start_at='07:00',
                end_at='17:00'
            )
            workday_6 = SpecialistWorkDayInSalon.objects.create(
                workday="2025-01-01",
                salon=salon_3,
                specialist=specialist_2,
                start_at='08:00',
                end_at='18:00'
            )
            workday_7 = SpecialistWorkDayInSalon.objects.create(
                workday="2025-01-02",
                salon=salon_1,
                specialist=specialist_3,
                start_at='08:00',
                end_at='18:00'
            )
            workday_8 = SpecialistWorkDayInSalon.objects.create(
                workday="2025-01-10",
                salon=salon_2,
                specialist=specialist_3,
                start_at='07:00',
                end_at='17:00'
            )
            workday_9 = SpecialistWorkDayInSalon.objects.create(
                workday="2024-12-29",
                salon=salon_3,
                specialist=specialist_3,
                start_at='08:00',
                end_at='18:00'
            )
            workday_10 = SpecialistWorkDayInSalon.objects.create(
                workday="2025-01-02",
                salon=salon_1,
                specialist=specialist_4,
                start_at='08:00',
                end_at='18:00'
            )
            workday_11 = SpecialistWorkDayInSalon.objects.create(
                workday="2024-10-28",
                salon=salon_2,
                specialist=specialist_4,
                start_at='07:00',
                end_at='17:00'
            )
            workday_12 = SpecialistWorkDayInSalon.objects.create(
                workday="2024-11-29",
                salon=salon_3,
                specialist=specialist_4,
                start_at='08:00',
                end_at='18:00'
            )
            workday_13 = SpecialistWorkDayInSalon.objects.create(
                workday="2024-12-28",
                salon=salon_1,
                specialist=specialist_5,
                start_at='08:00',
                end_at='18:00'
            )
            workday_14 = SpecialistWorkDayInSalon.objects.create(
                workday="2024-12-30",
                salon=salon_2,
                specialist=specialist_5,
                start_at='07:00',
                end_at='17:00'
            )
            workday_15 = SpecialistWorkDayInSalon.objects.create(
                workday="2024-12-31",
                salon=salon_3,
                specialist=specialist_5,
                start_at='08:00',
                end_at='18:00'
            )
            workday_16 = SpecialistWorkDayInSalon.objects.create(
                workday="2024-12-28",
                salon=salon_1,
                specialist=specialist_6,
                start_at='08:00',
                end_at='18:00'
            )
            workday_17 = SpecialistWorkDayInSalon.objects.create(
                workday="2024-12-30",
                salon=salon_2,
                specialist=specialist_6,
                start_at='07:00',
                end_at='17:00'
            )
            workday_18 = SpecialistWorkDayInSalon.objects.create(
                workday="2024-12-31",
                salon=salon_3,
                specialist=specialist_6,
                start_at='08:00',
                end_at='18:00'
            )

            # Создание записей
            appointment_1 = Appointment.objects.create(status='accepted', date='2024-12-30', salon=salon_3, client=client_1, specialist=specialist_6, service=service_1, start_at='10:00')
            appointment_2 = Appointment.objects.create(status='accepted', date='2024-12-30', salon=salon_3, client=client_2, specialist=specialist_6, service=service_2, start_at='12:00')
            appointment_3 = Appointment.objects.create(status='accepted', date='2024-12-30', salon=salon_3, client=client_3, specialist=specialist_6, service=service_3, start_at='14:00')
            appointment_4 = Appointment.objects.create(status='ended', date='2024-12-25', salon=salon_3, client=client_4, specialist=specialist_5, service=service_3, start_at='16:00')
            appointment_5 = Appointment.objects.create(status='ended', date='2024-12-25', salon=salon_3, client=client_5, specialist=specialist_5, service=service_4, start_at='18:00')
            appointment_6 = Appointment.objects.create(status='discard', date='2025-01-01', salon=salon_1, client=client_6, specialist=specialist_4, service=service_1, start_at='10:00')
            appointment_7 = Appointment.objects.create(status='discard', date='2025-01-01', salon=salon_1, client=client_7, specialist=specialist_4, service=service_2, start_at='12:00')

            # Создание счётов
            Order.objects.create(appointment=appointment_1, status='waiting', receipt='https://google.com')
            Order.objects.create(appointment=appointment_2, status='paid', receipt='https://google.com')
            Order.objects.create(appointment=appointment_3, status='cancel', receipt='https://google.com')
            Order.objects.create(appointment=appointment_4, status='waiting', receipt='https://google.com')
            Order.objects.create(appointment=appointment_5, status='paid', receipt='https://google.com')
            Order.objects.create(appointment=appointment_6, status='cancel', receipt='https://google.com')
            Order.objects.create(appointment=appointment_7, status='paid', receipt='https://google.com')
            self.stdout.write(self.style.SUCCESS(f'Тестовые данные успешно загружены в бд'))