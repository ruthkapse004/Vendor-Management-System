from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from datetime import datetime


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
        return Response({"Error": "No Vendor found with requested vendor_code."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        vendor_code = kwargs.get('pk')
        try:
            instance = self.get_queryset().get(vendor_code=vendor_code)
        except ObjectDoesNotExist:
            return Response({"Error": "No Vendor found with requested vendor_code."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        vendor_code = kwargs.get('pk')
        try:
            instance = self.get_queryset().get(vendor_code=vendor_code)
            instance.delete()
        except ObjectDoesNotExist:
            return Response({"Error": f"No Vendor found with requested vendor_code."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"Error": ex}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Detail": "Vendor deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


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
        except ObjectDoesNotExist:
            return Response({"Error": "No order found with requested po_number."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        po_number = kwargs.get('pk')
        try:
            instance = self.get_queryset().get(po_number=po_number)
            instance.delete()
        except ObjectDoesNotExist:
            return Response({"Error": "No order found with requested po_number."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def acknowledge_po(request, po_number):
    try:
        purchase_order = PurchaseOrder.objects.get(po_number=po_number)
    except:
        return Response({"Error": "No order found with requested po_number."}, status=status.HTTP_404_NOT_FOUND)

    if not purchase_order.acknowledgment_date:
        purchase_order.acknowledgment_date = datetime.now()
        purchase_order.save()
        return Response({"Success": "Your PO is acknowledged."}, status=status.HTTP_201_CREATED)
    else:
        return Response({"Detail": "Your PO is already acknowledged."}, status=status.HTTP_208_ALREADY_REPORTED)
