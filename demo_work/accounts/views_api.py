from django.core.validators import URLValidator
from requests import get
from accounts.models import Shop, CustomUser
from category.models import Category, CategoryShop
from product.models import ProductInfo, Product, Parameter, ProductParameter
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from yaml import load as load_yaml, Loader
from accounts.serializers import UserSerializer
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


class UpdateCatalog(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Error': 'Login required'}, status=401)
        if request.user.type != 'shop':
            return JsonResponse({'Error': 'User\'s type "shop" only'}, status=401)
        url = request.data['url']
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'Error': str(e)}, status=400)
            else:
                stream = get(url).content
                data = load_yaml(stream, Loader=Loader)

                shop = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
                for category in data['categories']:
                    category_object = Category.objects.get_or_create(id=category['id'],
                                                                     category=category['name'])
                    category_shop = CategoryShop.object.get_or_create(category_id=category_object.id,
                                                                      shop_id=shop.id)
                ProductInfo.objects.filter(shop_id=shop.id).delete()
                for item in data['goods']:
                    product = Product.odjects.get_or_create(name=item['name'],
                                                            category_id=item['category'])
                    product_info = ProductInfo.odjects.get_or_create(product_id=product.id,
                                                                     external_id=item['id'],
                                                                     shop_id=shop.id,
                                                                     price=item['price'],
                                                                     quantity=item['quantity'])
                    for name, value in item['parameters'].items():
                        parameter_object = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(product_info_id=product_info.id,
                                                        parameter_id=parameter_object.id,
                                                        value=value)
                return JsonResponse({'Msg': 'all create'}, status=201)
        return JsonResponse({'Errors': 'Url error. Not specified basic arguments'})
