from django.urls import path

from Payment.views import make_payment, all_payments, generate_report

urlpatterns = [
    path('make_payment/', make_payment, name='make_payment'),
    path('all_payments/', all_payments, name='payment_list'),
    path('generate_report/', generate_report, name='generate_report'),
]
