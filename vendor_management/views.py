from django.db.models.manager import BaseManager
from django.http.request import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PerformanceSerializer, PurchaseOrderSerializer
from datetime import datetime


# Create your views here.
class VendorViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'post', 'delete']

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    # context passed to serializer to access request inside serializer.
    def get_serializer_context(self) -> dict[str, HttpRequest]:
        return {'request': self.request}

    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = None
        # Assume product_code is used instead of id
        vendor_code = kwargs.get('pk')
        if vendor_code is not None:
            queryset = self.filter_queryset(self.get_queryset())
            instance = queryset.filter(vendor_code=vendor_code).first()
            if instance is not None:
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
        return Response({"Error": "No Vendor found with requested vendor_code."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs) -> Response:
        vendor_code = kwargs.get('pk')
        try:
            instance = self.get_queryset().get(vendor_code=vendor_code)
        except instance.DoesNotExist:
            return Response({"Error": "No Vendor found with requested vendor_code."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs) -> Response:
        vendor_code = kwargs.get('pk')
        try:
            instance = self.get_queryset().get(vendor_code=vendor_code)
            instance.delete()
        except instance.DoesNotExist:
            return Response({"Error": f"No Vendor found with requested vendor_code."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"Error": ex}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Detail": "Vendor deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class PurchaseOrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'post', 'delete']

    serializer_class = PurchaseOrderSerializer

    def get_queryset(self) -> BaseManager[PurchaseOrder]:
        queryset = PurchaseOrder.objects.all()
        vendor = self.request.query_params.get('vendor')
        if vendor:
            queryset = queryset.filter(vendor=vendor)
        return queryset

    def retrieve(self, request, *args, **kwargs) -> Response:
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

    def update(self, request, *args, **kwargs) -> Response:
        if request.data['status'] == "D" and not request.data['quality_rating']:
            return Response({"Error": "Quality rating not provided."}, status=status.HTTP_400_BAD_REQUEST)
        po_number = kwargs.get('pk')
        if request.data['status'] == "D" and PurchaseOrder.objects.filter(po_number=po_number, acknowledgment_date__isnull=True).exists():
            return Response({"Error": "PO is not acknowledged by the vendor."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = self.get_queryset().get(po_number=po_number)
        except instance.DoesNotExist:
            return Response({"Error": "No order found with requested po_number."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs) -> Response:
        po_number = kwargs.get('pk')
        try:
            instance = self.get_queryset().get(po_number=po_number)
            instance.delete()
        except instance.DoesNotExist:
            return Response({"Error": "No order found with requested po_number."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def acknowledge_po(request, po_number) -> Response:
    permission_classes = [IsAuthenticated]
    try:
        purchase_order = PurchaseOrder.objects.get(po_number=po_number)
    except PurchaseOrder.DoesNotExist:
        return Response({"Error": "No order found with requested po_number."}, status=status.HTTP_404_NOT_FOUND)

    if not purchase_order.acknowledgment_date:
        purchase_order.acknowledgment_date = datetime.now()
        purchase_order.save()
        return Response({"Success": "Your PO is acknowledged."}, status=status.HTTP_201_CREATED)
    else:
        return Response({"Detail": "Your PO is already acknowledged."}, status=status.HTTP_208_ALREADY_REPORTED)


class PerformanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_code) -> Response:
        try:
            vendor = Vendor.objects.get(vendor_code=vendor_code)
            serializer = PerformanceSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({"Error": "No Vendor found with requested vendor_code."}, status=status.HTTP_404_NOT_FOUND)
