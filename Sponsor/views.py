from django.shortcuts import render, redirect

from Sponsor.forms import SponsorForm
from User.mixins import user_type_required
from club.models import Club


# Create your views here.
@user_type_required(['marketer','admin'])
def add_sponsor(request):
    if request.method == 'POST':
        form = SponsorForm(request.POST, request.FILES)
        if form.is_valid():
            sponsor = form.save()

            # Обновление бюджета клуба
            club = Club.objects.first()  # Получение первого клуба (может потребоваться изменение этой логики)
            club.budget += sponsor.payment_amount  # Увеличение бюджета клуба на сумму платежа спонсора
            club.save()

            return redirect('marketer_dashboard')
    else:
        form = SponsorForm()
    return render(request, 'add_sponsor.html', {'form': form})