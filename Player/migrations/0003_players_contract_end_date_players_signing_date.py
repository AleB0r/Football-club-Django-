# Generated by Django 5.0.6 on 2024-05-12 18:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Player', '0002_remove_players_contract_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='players',
            name='contract_end_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='players',
            name='signing_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
