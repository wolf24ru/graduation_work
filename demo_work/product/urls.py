
from product.views_api import AddProducts, UpdateCatalog
from django.urls import path

urlpatterns = [
    path('add_products/', AddProducts.as_view(), name='add_products'),
    path('update_catalog/', UpdateCatalog.as_view(), name='update_catalog'),
]