from django.db import models

class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='sponsor_logos/')
    signing_date = models.DateField()
    cooperation_end_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
