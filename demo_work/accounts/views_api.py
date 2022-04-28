from accounts.models import Shop, CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from accounts.serializers import UserSerializer, ShopSerializer
from rest_framework.authtoken.models import Token

from django.http import JsonResponse


class RegistrationUser(APIView):
    """Регистрация пользователя"""
    queryset = CustomUser.objects.none()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        _argument_dict = {'first_name', 'last_name', 'email',
                          'password', 'company', 'position', 'username'}
        _required_argument = {'password', 'email', 'company'}
        data_in_dict = set(request.data)
        if data_in_dict.issubset(_argument_dict):
            if _required_argument.issubset(data_in_dict):
                try:
                    validate_password(request.data['password'])
                except Exception as password_error:
                    error_array = []
                    for item in password_error:
                        error_array.append(item)
                    return JsonResponse({'Error': {'password': error_array}})
                else:
                    user_serializer = UserSerializer(data=request.data)
                    if user_serializer.is_valid():
                        user = user_serializer.save()
                        user.set_password(request.data['password'])
                        user.save()
                        return JsonResponse({'Inform': 'User successful create'},
                                            status=201)
                    else:
                        return JsonResponse({'Error': user_serializer.errors})
            else:
                JsonResponse({'Error': 'entered  do not full list of argument'})
        else:
            JsonResponse({'Error': 'unexpected argument'})


class UserFilling(APIView):
    """Информация о пользователи

    GET: Получить информацию о пользователи
    POST: изменить информацию о пользователи
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Error': 'Login required'}, status=403)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Error': 'Login required'}, status=403)

        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({'Status': True})
        else:
            return JsonResponse({'Errors': user_serializer.errors})


class ShopView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Shop.objects.filter(order_accepting=True)
    serializer_class = ShopSerializer
#
# class UserInfo(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, *args, **kwargs):
#         user = CustomUser.objects.get(id=request.user.id)
#         content = {
#             'user': str(request.user.id),  # `django.contrib.auth.User` instance.
#             'auth': str(request.auth),  # None
#             'qeryset_user': {
#                 'email': user.email,
#                 'username': user.username,
#                 'company': user.company,
#                 'position': user.position,
#                 'is_admin': user.is_admin,
#                 'type': user.type
#             },
#         }
#         return JsonResponse(content)

