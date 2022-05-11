
# from rest_framework.routers import DefaultRouter
from accounts.views_api import UserFilling, RegistrationUser, ShopView,\
    VendorStatus, ContactView, NewToken
#
# router = DefaultRouter()
# router.register('user_info', UserInfo, 'user_info')
# router.register('login', Login, 'login')
#
# urlpatterns = router.urls

from django.urls import path

urlpatterns = [
    # path('user_info/', UserInfo.as_view(), name='user_info'),
    path('user_filling/', UserFilling.as_view(), name='user_filling'),
    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('shops/', ShopView.as_view(), name='shops'),
    path('shop/order_accepting', VendorStatus.as_view(), name='order_accepting'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('new_token/', NewToken.as_view(), name='new_token'),
]
