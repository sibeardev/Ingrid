import uuid

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Salon, Specialist, Service
from .forms import ConsultationForm
from ingrid.settings import API_YUMANI_KEY, SHOP_ID

from yookassa import Configuration, Payment


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
    return render(request, "service.html")


def service_finally(request: HttpRequest) -> HttpResponse:
    return render(request, "serviceFinally.html")


def payment(request):
    """Оплата заказа."""
    Configuration.account_id = SHOP_ID
    Configuration.secret_key = API_YUMANI_KEY
    payment = Payment.create({
        "amount": {
            "value": "100",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://127.0.0.1:8000/notes/"
        },
        "capture": True,
        "description": "Оплата заказа"
    }, uuid.uuid4())
    return HttpResponseRedirect(payment.confirmation.confirmation_url)
