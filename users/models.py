from django.db import models
from django.contrib.auth.models import AbstractUser

from materials.models import Course, Lesson
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', )
    avatar = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name='Аватар', )
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='Номер телефона', )
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Город')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payments(models.Model):
    CASH = 'Наличные'
    TRANSFER = 'Перевод'

    STATUS_CHOICES = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод'),
    ]

    date_payment = models.DateTimeField(auto_now_add=True, verbose_name='Дата платежа')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='оплаченный урок')
    amount_payment = models.PositiveIntegerField(verbose_name='Сумма оплаты', blank=True, null=True)
    method_payment = models.CharField(max_length=250, choices=STATUS_CHOICES, default=CASH,
                                      verbose_name='Способ оплаты')
    session_id = models.CharField(max_length=250, blank=True, null=True, verbose_name='ID сессии')
    link = models.URLField(max_length=400, blank=True, null=True, verbose_name='Ссылка на оплату')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_payments',
                              verbose_name='Владелец')

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return self.method_payment, self.amount
