
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse
from requests import get
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from yaml import load as load_yaml, Loader

from accounts.models import Shop
from category.models import Category
from category.models import CategoryShop
from product.models import ProductInfo, Product, Parameter, ProductParameter
from product.serializers import ProductSerializer, ProductInfoSerializer


class AddProducts(APIView):
    """Добавление продуктов
    {data:
        products:
        [{

        img: product_img,
        product:
            {
                name: product_name,
                category: product_category,
            },
        product_parameters:
            {
                parameter: product_parameter,
                value: product_value
            },
        price: product_price
        quantity: product_quantity
        }]
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Error': 'Login required'}, status=401)
        if request.user.type != 'shop':
            return JsonResponse({'Error': 'User\'s type "shop" only'}, status=401)
        try:
            products = request.data['products']
        except KeyError as e:
            return JsonResponse({'Error': f'not exist parameter: {e}'}, status=401)
        else:
            if type(products) is list and len(products) < 4:
                for product in products:
                    serializer = ProductInfoSerializer(data=product)
                    if not serializer.is_valid():
                        return JsonResponse({'Error': serializer.errors}, status=401)

                products_set = ProductInfo.objects.prefetch_related('product_parameters__parameter',
                                                                    'product_parameters',
                                                                    'img')
                print(product)
                parameters_list = []
                for _parameter in product['product_parameters']:
                    parameters_list.append(Parameter(name=_parameter["parameter"]))

                    # for category in data['categories']:
                    #     category_object = Category.objects.get_or_create(id=category['id'],
                    #                                                      category=category['name'])
                    #     CategoryShop.object.get_or_create(category_id=category_object.id,
                    #                                       shop_id=shop.id)
                    # ProductInfo.objects.filter(shop_id=shop.id).delete()
                    # for item in data['goods']:
                    #     product = Product.odjects.get_or_create(name=item['name'],
                    #                                             category_id=item['category'])
                    #     product_info = ProductInfo.odjects.get_or_create(product_id=product.id,
                    #                                                      external_id=item['id'],
                    #                                                      shop_id=shop.id,
                    #                                                      price=item['price'],
                    #                                                      quantity=item['quantity'])
                    #     for name, value in item['parameters'].items():
                    #         parameter_object = Parameter.objects.get_or_create(name=name)
                    #         ProductParameter.objects.create(product_info_id=product_info.id,
                    #                                         parameter_id=parameter_object.id,
                    #                                         value=value)
                    # return JsonResponse({'Msg': 'all create'}, status=201)
                    #

            elif len(products) >= 4:
                JsonResponse({'msg': 'For add more then 4 products use method UpdateCatalog'}, status=401)
            else:
                JsonResponse({'Error': 'bad request'}, status=401)
        return JsonResponse({'ok': 'ok'})


class UpdateCatalog(APIView):

    """обновление католога

    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Error': 'Login required'}, status=401)
        if request.user.type != 'shop':
            return JsonResponse({'Error': 'User\'s type "shop" only'}, status=401)
        try:
            url = request.data['url']
        except KeyError as e:
            return JsonResponse({'Error': f'not exist parameter: {e}'}, status=401)
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
                    CategoryShop.object.get_or_create(category_id=category_object.id,
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


class ProductInfoView(APIView):
    """
    quert_params:{
        'shop_id': id,
        'category_id': id
        }
    """
    queryset = ProductInfo.objects.none()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        query = Q(shop__order_accepting=True)
        try:
            shop_id = request.quert_params['shop_id']
            category_id = request.quert_params['category_id']
        except KeyError as e:
            return JsonResponse({'Error': f'not exist parameter: {e}'}, status=401)
        else:
            if shop_id:
                query = query & Q(shop_id=shop_id)

            if category_id:
                query = query & Q(product__category_id=category_id)

            queryset = not ProductInfo.objects.filter(query).\
                select_related('product__category', 'shop').\
                prefetch_related('product_parameters__parameter', 'img').\
                distinct()

            serializer = ProductInfoSerializer(queryset, many=True)
            return Response(serializer.data)
