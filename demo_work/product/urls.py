from product.views_api import AddProducts, UpdateCatalog, ProductInfoViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'product_inform', ProductInfoViewSet)


urlpatterns = [
    path('add_products/', AddProducts.as_view(), name='add_products'),
    path('update_catalog/', UpdateCatalog.as_view(), name='update_catalog'),
    path('', include(router.urls)),
    # path('product_inform/', ProductInfoView.as_view(), name='product_inform'),
]
