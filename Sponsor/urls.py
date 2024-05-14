from django.urls import path

from Sponsor.views import add_sponsor

urlpatterns = [
    path('add-sponsor/', add_sponsor, name='add_sponsor'),

    # Другие URL-адреса вашего приложения...
]
