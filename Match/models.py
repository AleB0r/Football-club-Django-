from django.db import models

class Match(models.Model):
    match_date = models.DateField()
    sold_tickets = models.PositiveIntegerField(default=0)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchased_vip_zones = models.PositiveIntegerField(default=0)
    vip_zone_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Match on {self.match_date}"
