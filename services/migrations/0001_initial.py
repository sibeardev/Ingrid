# Generated by Django 5.1.4 on 2024-12-20 20:32

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='RU', unique=True, verbose_name='Номер телефона')),
                ('full_name', models.CharField(max_length=200, verbose_name='ФИО')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='RU', verbose_name='Номер телефона')),
                ('question', models.CharField(blank=True, max_length=300, null=True, verbose_name='Вопрос')),
                ('consulted', models.BooleanField(default=False, verbose_name='Проконсультирован')),
            ],
            options={
                'verbose_name': 'Консультация',
                'verbose_name_plural': 'Консультация',
                'ordering': ['consulted'],
            },
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название салона')),
                ('address', models.TextField(max_length=200, verbose_name='Адрес салона')),
                ('image', models.ImageField(blank=True, db_index=True, upload_to='salon_images/', verbose_name='Баннер салона')),
            ],
            options={
                'verbose_name': 'Салон',
                'verbose_name_plural': 'Салоны',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название услуги')),
                ('price', models.IntegerField(verbose_name='Цена услуги')),
                ('duration', models.IntegerField(verbose_name='Длительность услуги, мин')),
                ('image', models.ImageField(blank=True, db_index=True, upload_to='service_images/', verbose_name='Банер услуги')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название типа услуги')),
            ],
            options={
                'verbose_name': 'Тип услуги',
                'verbose_name_plural': 'Типы услуг',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('accepted', 'Принято'), ('ended', 'Завершено'), ('discard', 'Отменено')], default='accepted', max_length=9, verbose_name='Статус заказа')),
                ('date', models.DateField(verbose_name='Дата записи')),
                ('start_at', models.TimeField(verbose_name='Время начала')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='appointments', to='services.client', verbose_name='Клиент')),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='appointments', to='services.salon', verbose_name='Салон')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='appointments', to='services.service', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Заказ услуги',
                'verbose_name_plural': 'Заказ услуг',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('waiting', 'Ожидает оплаты'), ('paid', 'Оплачено'), ('cancel', 'Отменено')], default='waiting', max_length=14, verbose_name='Статус заказа')),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Сумма заказа')),
                ('receipt', models.URLField(blank=True, verbose_name='Чек')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Счёт выставлен')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='services.appointment', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Счет оплаты',
                'verbose_name_plural': 'Счета оплаты',
            },
        ),
        migrations.AddField(
            model_name='service',
            name='s_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='services', to='services.servicetype', verbose_name='Тип услуги'),
        ),
        migrations.CreateModel(
            name='Specialist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, verbose_name='ФИО')),
                ('position', models.CharField(max_length=50, verbose_name='Специальность')),
                ('work_experience_years', models.IntegerField(default=0, verbose_name='Стаж (годы)')),
                ('work_experience_months', models.IntegerField(default=0, verbose_name='Стаж (месяцы)')),
                ('image', models.ImageField(blank=True, db_index=True, upload_to='specialist_images/', verbose_name='Фото мастера')),
                ('services', models.ManyToManyField(blank=True, related_name='specialists', to='services.service', verbose_name='Вид услуги')),
            ],
            options={
                'verbose_name': 'Специалист',
                'verbose_name_plural': 'Специалисты',
            },
        ),
        migrations.AddField(
            model_name='appointment',
            name='specialist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='appointments', to='services.specialist', verbose_name='Специалист'),
        ),
        migrations.CreateModel(
            name='SpecialistWorkDayInSalon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workday', models.DateField(verbose_name='Дата рабочего дня')),
                ('start_at', models.TimeField(verbose_name='Начало рабочего дня')),
                ('end_at', models.TimeField(verbose_name='Окончание рабочего дня')),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workdays', to='services.salon', verbose_name='Салон')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workdays', to='services.specialist', verbose_name='Специалист')),
            ],
            options={
                'verbose_name': 'Рабочий день',
                'verbose_name_plural': 'Рабочие дни',
            },
        ),
    ]
