
# from rest_framework.routers import DefaultRouter
from location.views_api import LocationInfor
from django.urls import path

urlpatterns = [
    path('location_inform/', LocationInfor.as_view(), name='location_inform'),
]
