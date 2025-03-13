from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
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