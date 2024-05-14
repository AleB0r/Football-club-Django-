from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404

from Player.forms import PlayerForm
from Player.models import Players
from User.mixins import user_type_required
from club.models import Club


# Create your views here.
@user_type_required(['sports_director'])
def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES)
        price = Decimal(request.POST.get('price', '0'))
        print(form.is_valid())
        if form.is_valid():
            club = Club.objects.first()  # Получение первого клуба (может потребоваться изменение этой логики)
            club.budget -= price  # Уменьшение бюджета клуба на сумму платежа спонсора
            club.save()
            form.save()
            return redirect('sport_dashboard')  # Перенаправляем на список игроков после успешного добавления
    else:
        form = PlayerForm()
    return render(request, 'add_player.html', {'form': form})

@user_type_required(['sports_director'])
def delete_player(request):
    if request.method == 'POST':
        try:
            player_id = request.POST.get('player_id')
            price = Decimal(request.POST.get('price', '0'))

            # Проверка, что price положителен
            if not price or float(price) <= 0:
                # Возвращаем ошибку или выполняем нужные действия в случае неправильного значения price
                # Например, можно добавить всплывающее сообщение об ошибке
                pass
            else:
                club = Club.objects.first()  # Получение первого клуба (может потребоваться изменение этой логики)
                club.budget += price  # Увеличение бюджета клуба на сумму платежа спонсора
                club.save()
                player = Players.objects.get(pk=player_id)
                player.delete()
        except Players.DoesNotExist:
            pass  # Обработка случая, когда пользователя не существует
    return redirect('sport_dashboard')

@user_type_required(['sports_director'])
def select_player(request):
    players = Players.objects.all()
    for player in players:
        print(player.id)
    return render(request, 'sell_player.html', {'players': players})

@user_type_required(['sports_director'])
def player_list(request):
    # Получаем список всех игроков
    players = Players.objects.all()
    # Передаем список игроков в шаблон для отображения
    return render(request, 'players_list.html', {'players': players})
