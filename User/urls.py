from django.urls import path
from django.http import Http404
from .views import login_view, create_user, admin_dashboard, delete_user, select_user, logout_user, marketer_dashboard, \
    sport_dashboard, accountant_dashboard, acces_404, ticket_sales_histogram, forgot_password

urlpatterns = [
    path('login/', login_view, name='login'),
    path('create/', create_user, name='create'),
    path('my-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('logout/', logout_user, name='logout'),
    path('select/', select_user, name='select_user'),
    path('delete/', delete_user, name='delete_user'),
    path('add_user/', create_user, name='add_user'),
    path('marketer/dashboard/', marketer_dashboard, name='marketer_dashboard'),
    path('sport_main/', sport_dashboard, name='sport_dashboard'),
    path('accountant/dashboard/', accountant_dashboard, name='accountant_dashboard'),
    path('analyse/', ticket_sales_histogram, name='analyse'),
    path('forgot/', forgot_password, name='forgot'),
    # Другие URL-адреса вашего приложения...
]


