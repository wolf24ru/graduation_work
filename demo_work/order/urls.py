from order.views_api import BasketView, VendorOrdersView, OrderView

from django.urls import path

urlpatterns = [
    path('basket/', BasketView.as_view(), name='basket'),
    path('vendor/', VendorOrdersView.as_view(), name='vendor'),
    path('get/', OrderView.as_view(), name='get_order'),

]
