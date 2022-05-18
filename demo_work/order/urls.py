from order.views_api import BasketViewSet, VendorOrdersView, OrderView
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'basket', BasketViewSet, basename='basket')

urlpatterns = [
    # path('basket/', BasketView.as_view(), name='basket'),
    path('', include(router.urls)),
    path('vendor/', VendorOrdersView.as_view(), name='vendor'),
    path('get/', OrderView.as_view(), name='get_order'),

]
