from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.offer_views import OfferViewSet, OfferDetailViewSet
from .views.order_views import OrderViewSet

router = DefaultRouter()
router.register(r'offers', OfferViewSet)
router.register(r'offerdetails', OfferDetailViewSet)
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]