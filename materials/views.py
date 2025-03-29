from datetime import timedelta
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwner, ModeratorPermission
from users.tasks import send_course_update_message


class CourseViewSet(viewsets.ModelViewSet):
    """Класс представления вида ViewSet для эндпоинтов курса."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all().order_by('id')
    pagination_class = MaterialsPagination

    def get_permissions(self):
        """Метод получения разрешений на доступ к эндпоитам в соответствии с запросом."""

        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated & ~ModeratorPermission]
        elif self.action in ['list', 'change', 'retrieve']:
            self.permission_classes = [IsAuthenticated & IsOwner | IsAuthenticated & ModeratorPermission]
        elif self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated & IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания "Курса"."""

        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

    def perform_update(self, serializer):
        """Метод вносит изменение в сериализатор редактирования "Курса"."""

        course = serializer.save()
        if course.updated_at:
            time_difference = timezone.now() - course.updated_at
            if time_difference > timedelta(hours=4):
                send_course_update_message.delay(course)
        else:
            send_course_update_message.delay(course)
        course.updated_at = timezone.now()
        course.save()

    def get_queryset(self):
        """Метод для изменения запроса к базе данных по объектам модели "Курса"."""

        if self.request.user.groups.filter(name="Модератор").exists():
            return Course.objects.all().order_by('id')
        return Course.objects.filter(owner=self.request.user)


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all().order_by('id')

    # def post(self, *args, **kwargs):
    #     # получаем пользователя
    #     user = self.requests.user
    #     # получаем id курса из self.requests.data
    #     course_id = self.requests.data.id
    #     # получаем объект курса из базы
    #     course_item = get_object_or_404(Course, id=course_id)
    #     # получаем объекты подписок по текущему пользователю и курса
    #     subs_item = get_object_or_404(Subscription, )
    #
    #     # Если подписка у пользователя на этот курс есть - удаляем ее
    #     if subs_item.exists():
    #         ...
    #         message = 'подписка удалена'
    #     # Если подписки у пользователя на этот курс нет - создаем ее
    #     else:
    #         ...
    #         message = 'подписка добавлена'
    #     # Возвращаем ответ в API
    #     return Response({"message": message})


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all().order_by('id')
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPagination

    def get(self, request):
        """ Пробую сделать пагинатор  """
        queryset = Lesson.objects.all().order_by('id')
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all().order_by('id')
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated & ModeratorPermission | IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all().order_by('id')
    serializer_class = LessonSerializer
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания "Урока"."""

        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated & ModeratorPermission | IsOwner]

    # def perform_update(self, serializer):
    #     """Метод вносит изменение в сериализатор редактирования "Урока"."""
    #
    #     lesson = serializer.save()
    #     courses = Course.objects.filter(id=lesson.course.pk)
    #     for course in courses:
    #         if lesson.updated_at:
    #             time_difference = timezone.now() - lesson.updated_at
    #             if time_difference > timedelta(hours=4):
    #                 send_course_update_message.delay(course.pk)
    #         else:
    #             send_course_update_message.delay(course.pk)
    #     lesson.updated_at = timezone.now()
    #     courses.updated_at = timezone.now()
    #     lesson.save()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated & ModeratorPermission | IsOwner]
