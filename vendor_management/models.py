from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from uuid import uuid4


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=256)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=256, unique=True, default=uuid4)
    on_time_delivery_rate = models.FloatField(default=None, null=True)
    quality_rating_avg = models.FloatField(default=None, null=True)
    average_response_time = models.FloatField(default=None, null=True)
    fulfillment_rate = models.FloatField(default=None, null=True)

    class Meta():
        db_table = 'vendor'

    def __str__(self) -> str:
        return self.name


class PurchaseOrder(models.Model):
    STATUS_DELIVERED = 'D'
    STATUS_CANCELED = 'C'
    STATUS_PENDING = 'P'
    STATUS_ISSUED = 'I'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ISSUED, 'PO Issued'),
        (STATUS_CANCELED, 'Canceled'),
        (STATUS_DELIVERED, 'Delivered'),
    ]

    po_number = models.CharField(max_length=256, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    order_date = models.DateField(auto_now_add=True)
    items = models.JSONField()
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)])
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    delivery_date = models.DateField()
    quality_rating = models.FloatField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    issue_date = models.DateTimeField(null=True)
    acknowledgment_date = models.DateTimeField(null=True)

    class Meta():
        db_table = 'purchase_order'

    def __str__(self) -> str:
        return self.po_number


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now=True)
    on_time_delivery_rate = models.FloatField(default=None, null=True)
    quality_rating_avg = models.FloatField(default=None, null=True)
    average_response_time = models.FloatField(default=None, null=True)
    fulfillment_rate = models.FloatField(default=None, null=True)

    class Meta():
        db_table = 'historical_performance'
