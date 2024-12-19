from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Salon, Specialist, Service
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
            print("Сообщение добавлено!")
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
    return render(request, "notes.html")


def service(request: HttpRequest) -> HttpResponse:
    return render(request, "service.html")


def service_finally(request: HttpRequest) -> HttpResponse:
    return render(request, "serviceFinally.html")


# def consultation(request):
#     if request.method == "POST":
#         name = request.POST.get('fname')
#         phone = request.POST.get('tel')
#         question = request.Post.get('contactsTextarea')
#         Consultation.objects.create(name=name, phone_number=phone, question=question)
#         messages.success(request, 'Запись на консультацию отправлена. Наш менеджер свяжется с вами в ближайшее время.')
#         return redirect('index')
#
#     return render(request, 'index.html')
