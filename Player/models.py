from django.db import models
from django.utils import timezone


class Players(models.Model):
    POSITION_CHOICES = (
        ('GK', 'Goalkeeper'),
        ('DF', 'Defender'),
        ('MF', 'Midfielder'),
        ('FW', 'Forward'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    squad_number = models.PositiveIntegerField(unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='player_photos/', null=True, blank=True)
    signing_date = models.DateField(default=timezone.now)
    contract_end_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"