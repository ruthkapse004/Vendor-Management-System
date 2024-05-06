# Generated by Django 5.0.4 on 2024-05-05 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_management', '0006_alter_purchaseorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperformance',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='order_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('I', 'PO Issued'), ('C', 'Canceled'), ('D', 'Delivered')], default='P', max_length=1),
        ),
    ]
