from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404

from User.mixins import user_type_required
from staff.forms import StaffForm
from staff.models import Staff


# Create your views here.
@user_type_required(['sports_director'])
def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')  # Перенаправляем на список персонала после успешного добавления
    else:
        form = StaffForm()
    return render(request, 'add_staff.html', {'form': form})

@user_type_required(['sports_director'])
def delete_staff(request):
    if request.method == 'POST':
        try:
            staff_id = request.POST.get('staff_id')
            staff = Staff.objects.get(pk=staff_id)
            staff.delete()
        except Staff.DoesNotExist:
            pass  # Обработка случая, когда пользователя не существует
    return redirect('sport_dashboard')

@user_type_required(['sports_director'])
def select_staff(request):
    staffes = Staff.objects.all()
    return render(request, 'select_staff.html', {'staffes': staffes})

@user_type_required(['sports_director'])
def staff_list(request):
    # Получаем список всех игроков
    staffes = Staff.objects.all()
    # Передаем список игроков в шаблон для отображения
    return render(request, 'staff_list.html', {'staffes': staffes})
