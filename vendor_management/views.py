from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from datetime import datetime, timedelta


# Create your views here.
class VendorViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'post', 'delete']

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    # context passed to serializer to access request inside serializer.
    def get_serializer_context(self):
        return {'request': self.request}

    def retrieve(self, request, *args, **kwargs):
        # Remove the default behavior of retrieving by pk
        instance = None
        # Assume product_code is used instead of pk
        vendor_code = kwargs.get('pk')
        if vendor_code is not None:
            queryset = self.filter_queryset(self.get_queryset())
            instance = queryset.filter(vendor_code=vendor_code).first()
            if instance is not None:
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
        return Response({"Error": "No Vendor matches the given query."}, status=status.HTTP_404_NOT_FOUND)


class PurchaseOrderViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'post', 'delete']

    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        vendor = self.request.query_params.get('vendor')
        if vendor:
            queryset = queryset.filter(vendor=vendor)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        # Remove the default behavior of retrieving by pk
        instance = None
        # Assume product_code is used instead of pk
        po_number = kwargs.get('pk')
        if po_number is not None:
            queryset = self.filter_queryset(self.get_queryset())
            instance = queryset.filter(po_number=po_number).first()
            if instance is not None:
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
        return Response({"Error": "No Order found with requested po_number."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        po_number = kwargs.get('pk')
        try:
            instance = self.get_queryset().get(po_number=po_number)
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "No order found with requested po_number."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        po_number = kwargs.get('pk')
        try:
            instance = self.get_queryset().get(po_number=po_number)
            instance.delete()
        except:
            return Response({"Error": "No order found with requested po_number."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
