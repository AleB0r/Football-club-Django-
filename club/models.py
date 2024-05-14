from django.db import models

class Club(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    stadium_name = models.CharField(max_length=100)
    stadium_capacity = models.IntegerField()
    vip_zones = models.PositiveIntegerField(default=0)  # Количество VIP-зон
    budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Бюджет клуба

    def __str__(self):
        return self.name
