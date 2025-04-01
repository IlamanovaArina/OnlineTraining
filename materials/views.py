from locale import currency
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from config import settings
from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPagination
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsOwner, ModeratorPermission
from users.services import create_stripe_product, modify_stripe_product
from users.tasks import send_course_update_message


class CourseViewSet(viewsets.ModelViewSet):
    """Класс представления вида ViewSet для эндпоинтов курса."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all().order_by('id')
    pagination_class = MaterialsPagination

    def log_update(self, course):
        # Логика для логирования обновлений
        print(f'Объект {course.id} был обновлен')
        print(f'Подробности: id: {course.id}, name: {course.name}, owner: {course.owner}, '
              f'updated_at: {course.updated_at}.')

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

        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.id_stripe_product = create_stripe_product(new_course).id
        new_course.save()


    def perform_update(self, serializer):
        """Метод вносит изменение в сериализатор редактирования "Курса"."""

        course = serializer.save()
        # self.log_update(course)
        course.updated_at = timezone.now()
        modify_stripe_product(course)
        course.save()

    def get_queryset(self):
        """Метод для изменения запроса к базе данных по объектам модели "Курса"."""

        if self.request.user.groups.filter(name="Модератор").exists():
            return Course.objects.all().order_by('id')
        return Course.objects.filter(owner=self.request.user)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """Класс представления вида ViewSet для эндпоинтов подписки."""
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all().order_by('id')

    def log(self, subscription, message):
        # Логика для логирования обновлений
        print(f'Объект {subscription.id} был {message}.')
        print(f'Подробности: id: {subscription.id}, course: {subscription.course}, user: {subscription.user}, '
              f'created_at: {subscription.created_at}.')

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания подписки."""
        user = self.request.user
        course = serializer.validated_data['course']  # Получаем курс из валидированных данных
        subscription = Subscription.objects.filter(owner=user, course=course, is_active=True).exists()

        # Проверяем, есть ли уже активная подписка на данный курс
        if subscription:
            return Response({"message": "У вас уже есть активная подписка на этот курс."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Если нет активной подписки, сохраняем новую
        subscription1 = serializer.save(owner=user)
        # self.log(subscription1, 'создан')
        return Response({"message": f"Подписка на курс: {course} добавлена."}, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        """Метод вносит изменение в сериализатор редактирования "Курса"."""

        course = serializer.save()
        # self.log(course, 'обновлён')
        course.updated_at = timezone.now()
        course.save()


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
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated & ModeratorPermission | IsOwner]


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
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated & ModeratorPermission | IsOwner]

    def update(self, request, *args, **kwargs):
        # Переопределяем метод update
        partial = kwargs.pop('partial', False)  # Для частичного обновления
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def log_update(self, lesson):
        # Логика для логирования обновлений
        print(f'Объект {lesson.id} был обновлен')
        print(f'Подробности: id: {lesson.id}, name: {lesson.name}, owner: {lesson.owner}, '
              f'updated_at: {lesson.updated_at}, course: {lesson.course}.')

    def perform_update(self, serializer):
        """Метод вносит изменение в сериализатор редактирования "Урока"."""

        lesson = serializer.save()
        # self.log_update(lesson)

        if lesson.course:
            lesson.courses.updated_at = timezone.now()
            lesson.courses.save()

        lesson.updated_at = timezone.now()
        lesson.save()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated & ModeratorPermission | IsOwner]
