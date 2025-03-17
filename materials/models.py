from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    preview = models.ImageField(upload_to='training/', blank=True, null=True, verbose_name='Превью')
    description = models.TextField(max_length=200, verbose_name='Описание')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    preview = models.ImageField(upload_to='training/', blank=True, null=True, verbose_name='Превью')
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name='Описание')
    link_to_video = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, blank=True, null=True, verbose_name='course')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name
