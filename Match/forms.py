from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Match

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['match_date', 'sold_tickets', 'ticket_price', 'purchased_vip_zones', 'vip_zone_price']
        widgets = {
            'match_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        match_date = cleaned_data.get('match_date')
        sold_tickets = cleaned_data.get('sold_tickets')
        purchased_vip_zones = cleaned_data.get('purchased_vip_zones')
        stadium_capacity = 50000  # Ваша вместимость стадиона
        vip_zones_count = 10  # Количество VIP-зон

        # Проверка на то, что дата матча не в будущем
        if match_date and match_date > timezone.now().date():
            raise ValidationError("Дата матча не может быть в будущем.")

        # Проверка на то, что количество проданных билетов не превышает вместимость стадиона
        if sold_tickets and sold_tickets > stadium_capacity:
            raise ValidationError("Количество проданных билетов не может превышать вместимость стадиона.")

        # Проверка на то, что количество купленных VIP-зон не превышает их количество
        if purchased_vip_zones and purchased_vip_zones > vip_zones_count:
            raise ValidationError("Количество купленных VIP-зон не может превышать их общее количество.")

        return cleaned_data