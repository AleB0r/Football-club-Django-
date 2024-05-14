from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrator'),
        ('sports_director', 'Sports Director'),
        ('marketer', 'Marketer'),
        ('accountant', 'Accountant'),
    )

    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)  # Добавляем поле для фотографии

    def __str__(self):
        return self.username
