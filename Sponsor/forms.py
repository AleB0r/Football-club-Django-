from django import forms
from django.utils import timezone
from .models import Sponsor

class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = '__all__'
        widgets = {
            'signing_date': forms.DateInput(attrs={'type': 'date'}),
            'cooperation_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        signing_date = cleaned_data.get('signing_date')
        cooperation_end_date = cleaned_data.get('cooperation_end_date')

        # Проверка, что дата подписания меньше сегодняшней даты
        if signing_date and signing_date > timezone.now().date():
            raise forms.ValidationError("Дата подписания не может быть в будущем.")

        # Проверка, что дата подписания меньше даты окончания сотрудничества
        if signing_date and cooperation_end_date and signing_date >= cooperation_end_date:
            raise forms.ValidationError("Дата подписания должна быть раньше даты окончания сотрудничества.")
