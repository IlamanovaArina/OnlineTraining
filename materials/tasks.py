from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery import Celery, shared_task
from users.models import User
from datetime import timedelta
from django.utils import timezone
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
import smtplib

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def send_course_or_lesson_update_message(title, recipient_list, name):
    """Отправляет сообщение об обновлении материалов курса."""

    try:
        course_or_lesson = ""
        if name == 'Урок':
            course_or_lesson = 'уроке'
        if name == 'Курс':
            course_or_lesson = 'уроке'

        if len(recipient_list) == 0:
            recipient_list = ['ilamanova.arina@gmail.com']

        send_mail(
            subject=f'В {course_or_lesson} произошли изменения',
            message=f'В {course_or_lesson} "{title}" произошли изменения',
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=True
        )
        print("send_course_or_lesson_update_message: Выполнена успешно;)")
    except BadHeaderError:
        return HttpResponse('Обнаружен недопустимый заголовок.')
    except smtplib.SMTPException:
        raise smtplib.SMTPException


@app.task
def blocking_inactive_users():
    """Блокирует пользователей неактивных более 30 дней."""

    users = User.objects.filter(is_active=True)
    inactive_user = []
    today = timezone.now().today()
    for user in users:
        if user.last_login:
            if today - user.last_login.date() > timedelta(days=30):
                inactive_user.append(user.email)
                user.is_active = False
                user.save()
    recipient_list = [user.email for user in User.objects.filter(groups='Администратор')]
    try:
        send_mail(
            subject='Отключение не активных пользователей',
            message=f"Отключены пользователи: {', '.join(inactive_user)}.",
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=True
        )
        print(f"Отключены пользователи: {', '.join(inactive_user)}.")
    except BadHeaderError:
        return HttpResponse('Обнаружен недопустимый заголовок.')
    except smtplib.SMTPException:
        raise smtplib.SMTPException


@shared_task
def set_schedule(sender: Celery, **kwargs):
    """ Задача по расписанию: проверять и отключать пользователей, которые не входили в систему больше 30 дней """

    # Создаем интервал для повтора
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )

    # Создаем задачу для повторения
    PeriodicTask.objects.create(
        interval=schedule,
        name='Проверка авторизации пользователя.',
        task='materials.tasks.blocking_inactive_users',
    )

    # celery -A config worker -l INFO -P eventlet
    # celery -A config beat -l INFO -S django -P eventlet
