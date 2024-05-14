from django.urls import path

from Player.views import add_player, select_player, delete_player, player_list

urlpatterns = [
path('add_player/', add_player, name='add_player'),
path('select_player/', select_player, name='select_player'),
path('delete_player/', delete_player, name='delete_player'),
path('players_list/', player_list, name='player_list'),


    # Другие URL-адреса вашего приложения...
]
