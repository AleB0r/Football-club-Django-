from django.db import models

from User.models import CustomUser


class Payment(models.Model):
    payment_date = models.DateField()
    player_count = models.PositiveIntegerField(default=0)
    staff_count = models.PositiveIntegerField(default=0)

    player_payments = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    staff_payments = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)  # Разрешить пустое значение для payer

    @property
    def total_count(self):
        return self.player_count + self.staff_count

    @property
    def total_payments(self):
        return self.player_payments + self.staff_payments

    def __str__(self):
        return f"Payment on {self.payment_date}"
