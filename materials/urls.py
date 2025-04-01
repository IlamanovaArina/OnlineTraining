from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateAPIView,
                             LessonDestroyAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView, SubscriptionViewSet)

router = SimpleRouter()
router.register(r'course', CourseViewSet, basename='course')
router.register(r'subscription', SubscriptionViewSet, basename='subscription')

# ^course/$ [name='course-list']
# ^course\.(?P<format>[a-z0-9]+)/?$ [name='course-list']
# ^course/(?P<pk>[^/.]+)/$ [name='course-detail']
# ^course/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='course-detail']
# [name='api-root']


app_name = MaterialsConfig.name

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/<int:pk>/delite/', LessonDestroyAPIView.as_view(), name='lesson_delite'),
] + router.urls
