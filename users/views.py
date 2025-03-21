from rest_framework import viewsets
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


# class PaymentsViewSet(viewsets.ModelViewSet):
#     serializer_class = PaymentsSerializer
#     queryset = Payments.objects.all()
#     filter_backends = [SearchFilter, OrderingFilter]
#     search_filter = ['paid_course', 'paid_lesson', 'method_payment',]
#     ordering_filter = ['date_payment',]


class PaymentsListAPIView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_filter = ['paid_course', 'paid_lesson', 'method_payment',]
    ordering_filter = ['date_payment',]


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]


class PaymentsCreateAPIView(generics.CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]


class PaymentsDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]