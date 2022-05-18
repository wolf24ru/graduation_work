from rest_framework.routers import DefaultRouter
from location.views_api import LocationInforViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'location_inform', LocationInforViewSet)

urlpatterns = [
    path('', include(router.urls))
    # path('location_inform/', LocationInfor.as_view(), name='location_inform'),
]
