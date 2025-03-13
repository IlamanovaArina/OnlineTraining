from django.urls import path

from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials.models import Lesson
from materials.serializers import LessonSerializer
from materials.views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')


app_name = MaterialsConfig.name

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(queryset=Lesson.objects.all(), serializer_class=LessonSerializer), name='user-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(queryset=Lesson.objects.all(), serializer_class=LessonSerializer), name='user-list'),
    path('lesson/create/', LessonCreateAPIView.as_view(queryset=Lesson.objects.all(), serializer_class=LessonSerializer), name='user-list'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(queryset=Lesson.objects.all(), serializer_class=LessonSerializer), name='user-list'),
    path('lesson/<int:pk>/delite/', LessonDestroyAPIView.as_view(queryset=Lesson.objects.all(), serializer_class=LessonSerializer), name='user-list'),
] + router.urls