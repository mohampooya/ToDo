# Generated by Django 3.2.23 on 2024-02-08 16:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklist',
            name='date_created',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
