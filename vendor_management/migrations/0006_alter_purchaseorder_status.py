# Generated by Django 5.0.4 on 2024-05-05 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_management', '0005_alter_historicalperformance_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('D', 'Delivered'), ('C', 'Canceled'), ('P', 'Pending'), ('I', 'Issued')], default='P', max_length=1),
        ),
    ]
