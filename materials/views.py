from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPagination
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsOwner, ModeratorPermission
from users.services import create_stripe_product, modify_stripe_product
from materials.tasks import send_course_or_lesson_update_message


class CourseViewSet(viewsets.ModelViewSet):
    """Класс представления вида ViewSet для эндпоинтов курса."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all().order_by('created_at').distinct()
    pagination_class = MaterialsPagination
    permission_classes = [AllowAny]

    def get_permissions(self):
        """Метод получения разрешений на доступ к эндпоитам в соответствии с запросом."""

        if self.action in ['create', 'put']:
            self.permission_classes = [IsAuthenticated | ModeratorPermission]
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

        subscriptions = Subscription.objects.filter(course=course.id)
        recipient_list = [subscriptions.owner.email for subscriptions in subscriptions]

        # Асинхронная отправка писем подписчикам курса, о произошедших обновлениях урока
        send_course_or_lesson_update_message.delay(course.name, recipient_list, 'Курс')
        # send_course_update_for_update_lesson_message.delay(course.name, recipient_list)

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
        serializer.save(owner=user)
        return Response({"message": f"Подписка на курс: {course} добавлена."}, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        """Метод вносит изменение в сериализатор редактирования "Курса"."""

        course = serializer.save()
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
    permission_classes = [IsAuthenticated & ModeratorPermission | IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all().order_by('id')
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания "Урока"."""

        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & ModeratorPermission | IsAuthenticated & IsOwner]

    def update(self, request, *args, **kwargs):
        # Переопределяем метод update
        partial = kwargs.pop('partial', False)  # Для частичного обновления
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        course_id = 0
        if request.data.get("course"):
            course_id = request.data.get("course")

        if course_id:
            subscriptions = Subscription.objects.filter(course=course_id)
            course = Course.objects.filter(id=course_id)
            recipient_list = [subscriptions.owner.email for subscriptions in subscriptions]

            # Асинхронная отправка писем подписчикам курса, о произошедших обновлениях урока
            send_course_or_lesson_update_message.delay(course[0].name, recipient_list, 'Урок')

        return Response(serializer.data)

    def perform_update(self, serializer):
        """Метод вносит изменение в сериализатор редактирования "Урока"."""

        lesson = serializer.save()

        if lesson.course:
            lesson.course.updated_at = timezone.now()
            lesson.course.save()

        lesson.updated_at = timezone.now()
        lesson.save()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & ModeratorPermission | IsOwner]
