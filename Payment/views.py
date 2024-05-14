from django.http import JsonResponse
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.utils import timezone

from Payment.models import Payment
from Player.models import Players
from User.mixins import user_type_required
from club.models import Club
from staff.models import Staff


from django.db.models import Sum
from django.http import JsonResponse
from django.utils import timezone

@user_type_required(['accountant'])
def make_payment(request):
    # Получаем пользователя, сделавшего выплату
    user = request.user

    # Проверяем, была ли выплата уже сделана в этом месяце
    today = timezone.now()
    current_month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_month_end = current_month_start.replace(month=current_month_start.month+1) - timezone.timedelta(days=1)
    if Payment.objects.filter(payment_date__range=(current_month_start, current_month_end)).exists():
        JsonResponse({'message': 'Выплата уже была сделана в текущем месяце.'}, status=400)
        return redirect('accountant_dashboard')

    # Вычисляем сумму зарплаты для игроков с действующим контрактом
    player_salary_total = Players.objects.filter(contract_end_date__gte=today).aggregate(total=Sum('salary'))['total'] or 0

    # Вычисляем сумму зарплаты для персонала с действующим контрактом
    staff_salary_total = Staff.objects.filter(hire_date__gte=today).aggregate(total=Sum('salary'))['total'] or 0

    # Суммируем общую сумму зарплаты
    total_payment_amount = player_salary_total + staff_salary_total

    # Вычитаем сумму выплаты из бюджета клуба
    club = Club.objects.first()  # Получаем первый клуб (может потребоваться изменение логики)
    club.budget -= total_payment_amount
    club.save()

    # Создаем запись о выплате
    Payment.objects.create(
        payment_date=today,
        payer=user,
        player_count=Players.objects.filter(contract_end_date__gte=today).count(),
        staff_count=Staff.objects.filter(hire_date__gte=today).count(),
        player_payments=player_salary_total,
        staff_payments=staff_salary_total,
    )

    # Возвращаем сообщение о успешном выполнении и общую сумму выплаты
    JsonResponse({'message': 'Выплата успешно выполнена.', 'total_payment_amount': total_payment_amount}, status=200)
    return redirect('accountant_dashboard')

@user_type_required(['accountant'])
def all_payments(request):
    payments = Payment.objects.all()
    return render(request, 'payment_list.html', {'payments': payments})
