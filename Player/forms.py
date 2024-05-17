from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Players

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Players
        fields = ['first_name', 'last_name', 'nationality', 'date_of_birth', 'position', 'squad_number', 'salary', 'signing_date', 'contract_end_date', 'photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'signing_date': forms.DateInput(attrs={'type': 'date'}),
            'contract_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_of_birth = cleaned_data.get('date_of_birth')
        signing_date = cleaned_data.get('signing_date')
        contract_end_date = cleaned_data.get('contract_end_date')

        # Проверка, что игроку больше 16 лет
        if date_of_birth:
            today = timezone.now().date()
            age_limit_date = today - timedelta(days=16*365)
            if date_of_birth > age_limit_date:
                raise forms.ValidationError("Игрок должен быть старше 16 лет.")

        # Проверка, что дата подписания меньше сегодняшней даты
        if signing_date and signing_date > timezone.now().date():
            raise forms.ValidationError("Дата подписания не может быть в будущем.")

        # Проверка, что дата подписания меньше даты окончания сотрудничества
        if signing_date and contract_end_date and signing_date >= contract_end_date:
            raise forms.ValidationError("Дата подписания должна быть раньше даты окончания сотрудничества.")

        return cleaned_data
