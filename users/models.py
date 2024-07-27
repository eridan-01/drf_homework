from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="Email")

    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        **NULLABLE,
        help_text="Загрузите фото",
    )
    phone_number = PhoneNumberField(
        **NULLABLE, verbose_name="Номер телефона", help_text="Введите номер телефона"
    )
    country = models.CharField(
        **NULLABLE, max_length=50, verbose_name="Город", help_text="Введите город"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHODS = (("cash", "Наличные"), ("transfer", "Перевод на счет"))

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
    )

    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")

    paid_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс", **NULLABLE
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок", **NULLABLE
    )

    amount = models.DecimalField(
        verbose_name="Сумма оплаты", max_digits=10, decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHODS,
        verbose_name="Метод оплаты",
        help_text="Выберите метод оплаты",
    )

    def __str__(self):
        return (
            f"{self.user}: {self.payment_date}, {self.amount}, {self.payment_method}, "
            f"за {self.paid_course if self.paid_course else self.paid_lesson}"
        )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
