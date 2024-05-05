# Generated by Django 5.0.4 on 2024-05-05 09:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_management', '0003_alter_vendor_vendor_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='quality_rating',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)]),
        ),
    ]