from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    """Клиент"""

    phone_number = PhoneNumberField("Номер телефона", region="RU", unique=True)
    full_name = models.CharField("ФИО", max_length=200)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self) -> str:
        return self.full_name


class Salon(models.Model):
    """Салон"""

    title = models.CharField("Название салона", max_length=100)
    address = models.TextField("Адрес салона", max_length=200)
    image = models.ImageField(
        "Баннер салона",
        upload_to="salon_images/",
        db_index=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Салон"
        verbose_name_plural = "Салоны"

    def __str__(self) -> str:
        return self.title


class Service(models.Model):
    """Услуга"""

    title = models.CharField("Название услуги", max_length=200)
    price = models.IntegerField("Цена услуги")
    duration = models.IntegerField("Длительность услуги, мин")
    image = models.ImageField(
        "Банер услуги",
        upload_to="service_images/",
        db_index=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self) -> str:
        return self.title


class Specialist(models.Model):
    """Специалист"""

    full_name = models.CharField("ФИО", max_length=200)
    position = models.CharField("Специальность", max_length=50)
    services = models.ManyToManyField(
        "Service", verbose_name="Вид услуги", related_name="specialists", blank=True
    )
    work_experience_years = models.IntegerField("Стаж (годы)", default=0)
    work_experience_months = models.IntegerField("Стаж (месяцы)", default=0)
    image = models.ImageField(
        "Фото мастера",
        upload_to="specialist_images/",
        db_index=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Специалист"
        verbose_name_plural = "Специалисты"

    def __str__(self) -> str:
        return self.full_name


class Order(models.Model):
    """Счёт (статус оплаты)"""

    STATUS = [
        ("waiting", "Ожидает оплаты"),
        ("paid", "Оплачено"),
        ("cancel", "Отменено"),
    ]

    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, verbose_name="Клиент", related_name="orders"
    )
    status = models.CharField(
        "Статус заказа", max_length=14, choices=STATUS, default="waiting"
    )
    total_amount = models.DecimalField(
        "Сумма заказа",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    receipt = models.URLField("Чек", blank=True)
    created_at = models.DateTimeField("Счёт выставлен", auto_now_add=True)
    updated_at = models.DateTimeField("Последнее обновление", auto_now=True)

    class Meta:
        verbose_name = "Счет оплаты"
        verbose_name_plural = "Счета оплаты"

    def __str__(self) -> str:
        return f"{self.updated_at} {self.client.full_name} {self.status}"


class SpecialistWorkDayInSalon(models.Model):
    """Рабочий день сотрудника в одном из салонов"""

    workday = models.DateField("Дата рабочего дня")
    salon = models.ForeignKey(
        Salon, on_delete=models.PROTECT, verbose_name="Салон", related_name="workdays"
    )
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.PROTECT,
        verbose_name="Специалист",
        related_name="workdays",
    )
    services = models.ManyToManyField(
        Service,
        verbose_name="Услуги",
    )
    start_at = models.TimeField("Начало рабочего дня")
    end_at = models.TimeField("Окончание рабочего дня")

    class Meta:
        verbose_name = "Рабочий день"
        verbose_name_plural = "Рабочие дни"

    def __str__(self) -> str:
        return f"{self.specialist} {self.salon} {self.workday}"


class Appointment(models.Model):
    """Заказ услуги"""

    STATUSES = [
        ("accepted", "Принято"),
        ("ended", "Завершено"),
        ("discard", "Отменено"),
    ]

    status = models.CharField(
        "Статус заказа", max_length=9, choices=STATUSES, default="accepted"
    )
    salon = models.ForeignKey(
        Salon,
        on_delete=models.PROTECT,
        verbose_name="Салон",
        related_name="appointments",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Клиент",
        related_name="appointments",
    )
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.PROTECT,
        verbose_name="Специалист",
        related_name="appointments",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        verbose_name="Услуга",
        related_name="appointments",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        verbose_name="Заказ",
        related_name="appointments",
    )
    date = models.DateField("Дата записи")
    start_at = models.TimeField("Время начала")

    class Meta:
        verbose_name = "Заказ услуги"
        verbose_name_plural = "Заказ услуг"

    def __str__(self) -> str:
        return f"{self.status} {self.date} {self.salon.title} {self.client.full_name}"


class Consultation(models.Model):
    """Ожидают консультацию"""

    name = models.CharField("Имя", max_length=50)
    phone_number = PhoneNumberField("Номер телефона", region="RU")
    question = models.CharField("Вопрос", max_length=300, blank=True, null=True)
    consulted = models.BooleanField("Проконсультирован", default=False)

    class Meta:
        verbose_name = "Консультация"
        verbose_name_plural = "Консультация"
        ordering = ["consulted"]

    def __str__(self) -> str:
        return f"{self.name} {self.consulted}"
