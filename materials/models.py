from django.db import models

from config import settings


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    id_stripe_product = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name='Название для оплаты')
    preview = models.ImageField(upload_to='training/', blank=True, null=True, verbose_name='Превью')
    description = models.TextField(max_length=200, verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1,
                              related_name='owner_course', verbose_name='Владелец')
    price = models.IntegerField(default=0, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    id_stripe_product = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name='Название для оплаты')
    preview = models.ImageField(upload_to='training/', blank=True, null=True, verbose_name='Превью')
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name='Описание')
    link_to_video = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, blank=True, null=True, verbose_name='course')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1,
                              related_name='owner_lesson', verbose_name='Владелец')
    price = models.IntegerField(default=0, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT, blank=True, null=True, verbose_name='course')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner_subscription',
                             default=1, verbose_name='Владелец')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата начала подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.course
