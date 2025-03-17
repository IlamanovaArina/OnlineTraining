from django.urls import path

from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')


app_name = MaterialsConfig.name

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/delite/', LessonDestroyAPIView.as_view(), name='lesson-delite'),
] + router.urls