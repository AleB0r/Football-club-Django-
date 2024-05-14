# Generated by Django 5.0.6 on 2024-05-12 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Player', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='players',
            name='contract_end_date',
        ),
        migrations.RemoveField(
            model_name='players',
            name='signing_date',
        ),
        migrations.AddField(
            model_name='players',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='player_photos/'),
        ),
    ]
