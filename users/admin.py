from django.contrib import admin

from users.models import User, Payments


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'avatar', 'phone', 'city',)
    list_filter = ('email', 'id')


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_payment', 'paid_course', 'paid_lesson', 'amount_payment', 'method_payment', 'owner')
    list_filter = ('id', 'paid_lesson', 'paid_course', 'date_payment',)
