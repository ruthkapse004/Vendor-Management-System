from rest_framework.viewsets import ModelViewSet
from .models import Vendor
from .serializers import VendorSerializer


# Create your views here.
class VendorViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'post', 'delete']

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
