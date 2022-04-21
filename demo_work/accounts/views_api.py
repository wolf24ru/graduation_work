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
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from yaml import load as load_yaml, Loader
from rest_framework.authtoken.models import Token

from django.http import JsonResponse


class UserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # user = CustomUser.objects.get()
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return JsonResponse(content)


class UpdateCatalog(APIView):
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
