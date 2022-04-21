
# from rest_framework.routers import DefaultRouter
from accounts.views_api import UserInfo, Login
#
# router = DefaultRouter()
# router.register('user_info', UserInfo, 'user_info')
# router.register('login', Login, 'login')
#
# urlpatterns = router.urls

from django.urls import path

urlpatterns = [
    path('user_info/', UserInfo.as_view(), name='user_info'),
    path('login/', Login.as_view(), name='login')
]
