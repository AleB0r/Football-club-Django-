from django.urls import path

from Match.views import add_match

urlpatterns = [
path('add_match/', add_match, name='add_match'),
    # Другие URL-адреса вашего приложения...
]
