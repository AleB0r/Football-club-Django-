from django.shortcuts import render, redirect

from User.mixins import user_type_required
from club.models import Club
from .models import Match
from .forms import MatchForm

@user_type_required(['sports_director'])
def add_match(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            # Сохраняем форму матча
            match = form.save()

            # Вычисляем доход от продажи билетов и VIP-зон
            ticket_income = match.sold_tickets * match.ticket_price
            vip_income = match.purchased_vip_zones * match.vip_zone_price
            total_income = ticket_income + vip_income

            # Обновляем бюджет клуба
            club = Club.objects.first()  # Предполагаем, что у нас есть только один клуб
            club.budget += total_income
            club.save()

            return redirect('sport_dashboard')  # Перенаправляем на список матчей после успешного добавления
    else:
        form = MatchForm()
    return render(request, 'add_match.html', {'form': form})
