from rest_framework import serializers
from datetime import datetime
from .models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):
    vendor_code = serializers.CharField(read_only=True)

    class Meta:
        model = Vendor
        fields = ['vendor_code', 'name', 'contact_details', 'address']


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_code', 'on_time_delivery_rate',
                  'quality_rating_avg', 'average_response_time', 'fulfillment_rate']


class RetrievePurchaseOrderSerializer(serializers.ModelSerializer):
    po_number = serializers.CharField(read_only=True)
    order_date = serializers.DateField(read_only=True)
    issue_date = serializers.DateTimeField(read_only=True)
    acknowledgment_date = serializers.DateTimeField(read_only=True)
    vendor_code = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor_code', 'order_date', 'delivery_date', 'items',
                  'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']

    def get_vendor_code(self, obj) -> str:
        return str(obj.vendor.vendor_code)


class PurchaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = ['vendor',  'delivery_date', 'items',
                  'quantity', 'status', 'quality_rating',]

    def save(self, **kwargs):
        request = self.context.get('request')

        # We add po_number & delivery_date only when for POST request.
        if request.method == "POST":
            # Generate the unique PO number
            po_number = "".join(str(datetime.now().timestamp()).split('.'))

            # Generate Expected or actual delivery date of the order.
            self.validated_data['issue_date'] = None
            self.validated_data['po_number'] = po_number
            self.validated_data['delivery_date'] = request.data['delivery_date']
        if request.method == "PUT":
            if request.data['status'] == "I":
                self.validated_data['issue_date'] = datetime.now()
            elif request.data['status'] == "D":
                now_date = datetime.now().date()
                self.validated_data['delivery_date'] = now_date
        return super().save(**kwargs)
