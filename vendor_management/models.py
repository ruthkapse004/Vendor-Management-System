from django.db import models


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=256)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=256, unique=True)
    on_time_delivery_rate = models.FloatField(default=None, null=True)
    quality_rating_avg = models.FloatField(default=None, null=True)
    average_response_time = models.FloatField(default=None, null=True)
    fulfillment_rate = models.FloatField(default=None, null=True)


class PurchaseOrder(models.Model):
    STATUS_COMPLETED = 'C'
    STATUS_CANCELED = 'D'
    STATUS_PENDING = 'P'

    STATUS_CHOICES = [
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELED, 'Canceled'),
        (STATUS_PENDING, 'Pending'),
    ]

    po_number = models.CharField(max_length=256, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True)


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField(default=None, null=True)
    quality_rating_avg = models.FloatField(default=None, null=True)
    average_response_time = models.FloatField(default=None, null=True)
    fulfillment_rate = models.FloatField(default=None, null=True)
