from rest_framework import serializers
from .models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):
    vendor_code = serializers.CharField(read_only=True)
    on_time_delivery_rate = serializers.FloatField(read_only=True)
    quality_rating_avg = serializers.FloatField(read_only=True)
    average_response_time = serializers.FloatField(read_only=True)
    fulfillment_rate = serializers.FloatField(read_only=True)

    class Meta:
        model = Vendor
        fields = ['vendor_code', 'name', 'contact_details', 'address', 'on_time_delivery_rate',
                  'quality_rating_avg', 'average_response_time', 'fulfillment_rate']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    po_number = serializers.CharField(read_only=True)
    order_date = serializers.DateTimeField(read_only=True)
    delivery_date = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    issue_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'order_date', 'delivery_date', 'items',
                  'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']
