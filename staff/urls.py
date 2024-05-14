from django.urls import path
from . import views

urlpatterns = [
    path('add_staff/', views.add_staff, name='add_staff'),
    path('delete_staff/', views.delete_staff, name='delete_staff'),
    path('select_staff/', views.select_staff, name='select_staff'),
    path('staff_list/', views.staff_list, name='staff_list'),
]
