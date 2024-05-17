from calendar import monthrange
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import LogoutView

from django.db.models import Avg, Sum, DecimalField, ExpressionWrapper, F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.utils import timezone

from Match.models import Match
from Payment.models import Payment
from Player.models import Players
from Sponsor.models import Sponsor
from club.models import Club
from staff.models import Staff
from .forms import CustomUserCreationForm
from .mixins import user_type_required
from .models import CustomUser  # Import your custom user model

def logout_user(request):
    logout(request)
    return redirect('login')

@user_type_required(['admin'])
def select_user(request):
    users = CustomUser.objects.all()
    for user in users:
        print(user.id)
    return render(request, 'select_user.html', {'users': users})

@user_type_required(['admin'])
def delete_user(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            user = CustomUser.objects.get(pk=user_id)
            user.delete()
        except CustomUser.DoesNotExist:
            pass  # Обработка случая, когда пользователя не существует
    return redirect('admin_dashboard')


@user_type_required(['admin'])
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Перенаправление на страницу успешного создания пользователя
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_user.html', {'form': form})


@user_type_required(['admin'])
def admin_dashboard(request):
    # Получаем информацию о количестве пользователей
    total_users = CustomUser.objects.count()

    # Получаем информацию о количестве игроков
    total_players = Players.objects.count()

    # Получаем информацию о количестве персонала
    total_staff = Staff.objects.count()

    # Получаем последние 10 зашедших пользователей
    recent_users = CustomUser.objects.order_by('-last_login')[:5]

    # Получаем количество пользователей, которые заходили сегодня
    today_users_count = CustomUser.objects.filter(last_login__date=timezone.now().date()).count()

    # Получаем последних 10 зарегистрированных пользователей
    latest_registered_users = CustomUser.objects.order_by('-date_joined')[:8]

    # Передаем данные в шаблон
    return render(request, 'admin_main.html', {
        'recent_users': recent_users,
        'total_users': total_users,
        'total_players': total_players,
        'total_staff': total_staff,
        'today_users_count': today_users_count,
        'latest_registered_users': latest_registered_users,
    })

@user_type_required(['marketer','admin'])
def marketer_dashboard(request):
    today = timezone.now().date()
    # Получаем всех активных спонсоров, с кем сотрудничество еще не закончилось
    active_sponsors = Sponsor.objects.filter(cooperation_end_date__gte=today)
    return render(request, 'marketer_main.html', {'active_sponsors': active_sponsors})

def acces_404(request, exception):
    return render(request, '404.html', status=404)


@user_type_required(['sports_director','admin'])
def sport_dashboard(request):
    # Получаем объект клуба (предположим, что это единственный клуб)
    club = Club.objects.first()

    # Получаем бюджет клуба
    club_budget = club.budget

    today = date.today()

    # Получаем количество игроков в клубе, у которых контракт еще действует
    player_count = Players.objects.filter(contract_end_date__gte=today).count()

    # Получаем последних подписанных игроков
    latest_signed_players = Players.objects.filter(contract_end_date__gte=today).order_by('-signing_date')[:5]

    # Получаем вместимость стадиона
    stadium_capacity = club.stadium_capacity

    latest_matches = Match.objects.filter().order_by('-match_date')[:8]

    # Передаем данные в шаблон
    return render(request, 'sport_dir_main.html', {
        'club_name': club.name,
        'club_budget': club_budget,
        'player_count': player_count,
        'latest_signed_players': latest_signed_players,
        'stadium_capacity': stadium_capacity,
        'latest_matches': latest_matches,
    })




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        print(username)

        # Проверяем, существует ли пользователь с таким именем
        if CustomUser.objects.filter(username=username).exists():  # Replaced User with CustomUser
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(user)
                # Определяем доступные страницы для различных типов пользователей
                if user.is_superuser:
                    return redirect('admin_dashboard')  # Например, страница администратора
                elif user.user_type == 'sports_director':
                    return redirect('sport_dashboard')  # Например, страница спортивного директора
                elif user.user_type == 'marketer':
                    return redirect('marketer_dashboard')  # Например, страница маркетолога
                elif user.user_type == 'accountant':
                    return redirect('accountant_dashboard')  # Например, страница бухгалтера
                else:
                    return redirect('regular_user_dashboard')  # Например, обычная страница для остальных пользователей
            else:
                # Если аутентификация не удалась, возвращаем страницу входа с сообщением об ошибке
                return render(request, 'auth.html', {'error_message': 'Invalid username or password'})
        else:
            print('hi')
            # Если пользователь с таким именем не найден, возвращаем страницу входа с сообщением об ошибке
            return render(request, 'auth.html', {'error_message': 'User does not exist'})
    else:
        return render(request, 'auth.html')

@user_type_required(['accountant','admin'])
def accountant_dashboard(request):
    # Получаем общее количество игроков
    total_players = Players.objects.filter(contract_end_date__gte=timezone.now()).count()

    # Получаем общее количество персонала
    total_staff = Staff.objects.filter(hire_date__gte=timezone.now()).count()

    # Получаем среднюю зарплату футболистов
    average_player_salary = Players.objects.filter(contract_end_date__gte=timezone.now()).aggregate(Avg('salary'))['salary__avg']

    # Получаем среднюю зарплату персонала
    average_staff_salary = Staff.objects.filter(hire_date__gte=timezone.now()).aggregate(Avg('salary'))['salary__avg']

    # Получаем бюджет клуба
    club_budget = Club.objects.first().budget

    total = total_staff + total_players

    # Получаем последние 8 выплат
    latest_payments = Payment.objects.order_by('-payment_date')[:8]

    # Передаем данные в шаблон
    return render(request, 'accountant_main.html', {
        'total': total,
        'average_player_salary': average_player_salary,
        'average_staff_salary': average_staff_salary,
        'club_budget': club_budget,
        'latest_payments': latest_payments,
    })

@user_type_required(['sports_director','admin'])
def ticket_sales_histogram(request):
    # Get the current date
    current_date = datetime.now()

    # Calculate the start date of the previous year
    start_date = current_date.replace(year=current_date.year - 1, month=current_date.month, day=1)

    # Initialize lists to store ticket sales and revenue data
    ticket_sales_data = []
    revenue_data = []

    # Loop through the last 12 months in reverse order
    for i in range(12, -1, -1):
        # Calculate the start and end dates for the current month
        month_start = start_date.replace(day=1)
        month_end = start_date.replace(day=monthrange(start_date.year, start_date.month)[1])
        print(month_start, month_end)

        # Get ticket sales for the current month
        month_sales = Match.objects.filter(match_date__range=[month_start, month_end]).aggregate(total_sales=Sum('sold_tickets'))['total_sales'] or 0
        print(month_sales)

        # Calculate revenue for the current month
        month_revenue = Match.objects.filter(
            match_date__range=[month_start, month_end]
        ).aggregate(
            month_revenue=Sum(ExpressionWrapper(
                F('sold_tickets') * F('ticket_price'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ))
        )['month_revenue'] or 0
        print(month_revenue)

        # Append data to lists
        ticket_sales_data.append(month_sales)
        revenue_data.append(month_revenue)

        # Move to the next month
        start_date += timedelta(days=monthrange(start_date.year, start_date.month)[1])

    # Reverse the lists to display data in chronological order
    ticket_sales_data.reverse()
    revenue_data.reverse()

    # Generate labels for the last 12 months starting from the current month
    months = [(current_date - timedelta(days=i * 30)).strftime('%b') for i in range(12)]

    return render(request, 'test.html', {
        'months': months,
        'ticket_sales_data': ticket_sales_data,
        'revenue_data': revenue_data,
    })


def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email="sasha2014993@gmail.com",
            )
            messages.success(request, 'Instructions for resetting your password have been emailed to you.')
            return redirect('login')  # Redirect to login page after sending reset instructions
    else:
        form = PasswordResetForm()
    return render(request, 'forget.html', {'form': form})