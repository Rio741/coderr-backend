from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.offer_views import OfferViewSet, OfferDetailViewSet
from .views.order_views import OrderViewSet
from .views.orderCount_views import OrderCountView, CompletedOrderCountView
from .views.baseInfo_view import BaseInfoView
from .views.review_views import ReviewViewSet

router = DefaultRouter()
router.register(r'offers', OfferViewSet)
router.register(r'offerdetails', OfferDetailViewSet)
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = [
    path('', include(router.urls)),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order_count'),
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='completed_order_count'),
    path('base-info/', BaseInfoView.as_view(), name='base_info'),
]