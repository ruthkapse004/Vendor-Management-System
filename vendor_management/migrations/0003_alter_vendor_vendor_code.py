# Generated by Django 5.0.4 on 2024-05-03 22:01

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_management', '0002_alter_historicalperformance_average_response_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vendor_code',
            field=models.CharField(default=uuid.uuid4, max_length=256, unique=True),
        ),
    ]