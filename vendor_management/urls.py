from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('vendors', views.VendorViewSet)
router.register('purchase_orders', views.PurchaseOrderViewSet,
                basename='purchase_orders')

urlpatterns = [
    path('', include(router.urls)),
    path('purchase_orders/<str:po_number>/acknowledge/', views.acknowledge_po),

]
