from django.db import models
from django.contrib.auth.models import AbstractUser

from materials.models import Course, Lesson


# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', )
    avatar = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name='Аватар', )
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='Номер телефона', )
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Город')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_payment = models.DateTimeField(auto_now_add=True, verbose_name='Дата платежа')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, verbose_name='оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True, verbose_name='оплаченный урок')
    amount_payment = models.IntegerField(verbose_name='Сумма оплаты')
    method_payment = models.CharField(choices=STATUS_CHOICES, default=CASH, verbose_name='Способ оплаты')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', default=1, verbose_name='Владелец')

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return self.method_payment
