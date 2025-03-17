from django.urls import path
from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, PaymentsListAPIView, PaymentsRetrieveAPIView, \
    PaymentsCreateAPIView, PaymentsUpdateAPIView, PaymentsDestroyAPIView

router = DefaultRouter()
# router.register(r'payments', PaymentsViewSet, basename='payments')
router.register(r'user', UserViewSet, basename='user')

app_name = UsersConfig.name

urlpatterns = [
      path('payments/', PaymentsListAPIView.as_view(), name='lesson-list'),
      path('payments/<int:pk>/', PaymentsRetrieveAPIView.as_view(), name='lesson'),
      path('payments/create/', PaymentsCreateAPIView.as_view(), name='lesson-create'),
      path('payments/<int:pk>/update/', PaymentsUpdateAPIView.as_view(), name='lesson-update'),
      path('payments/<int:pk>/delite/', PaymentsDestroyAPIView.as_view(), name='lesson-delite'),
] + router.urls
