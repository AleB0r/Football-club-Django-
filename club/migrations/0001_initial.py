# Generated by Django 5.0.6 on 2024-05-09 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('founded_year', models.IntegerField()),
                ('stadium_name', models.CharField(max_length=100)),
                ('stadium_capacity', models.IntegerField()),
                ('vip_zones', models.PositiveIntegerField(default=0)),
                ('budget', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
            ],
        ),
    ]