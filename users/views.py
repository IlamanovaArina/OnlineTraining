from rest_framework import viewsets
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.models import Payments, User
from users.permissions import ModeratorPermission, IsOwner
from users.serializers import PaymentsSerializer, UserSerializer
from users.services import create_stripe_product, create_stripe_session, create_stripe_price


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
    permission_classes = [IsAdminUser | IsOwner]
    filter_backends = [SearchFilter, OrderingFilter]
    search_filter = ['paid_course', 'paid_lesson', 'method_payment',]
    ordering_filter = ['date_payment',]


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAdminUser | IsOwner]


class PaymentsCreateAPIView(generics.CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Оплата покупки через stripe """
        payment = serializer.save(owner=self.request.user)
        course = payment.paid_course
        # price = payment.paid_course.price
        # id_stripe_product = payment.paid_course.id_stripe_product
        price = create_stripe_price(course.price, course.id_stripe_product)

        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.method_payment = "Перевод"
        payment.save()


class PaymentsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAdminUser]


class PaymentsDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAdminUser]
