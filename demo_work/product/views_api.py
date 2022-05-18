
import django
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import Q, ObjectDoesNotExist
from django.http import JsonResponse

from requests import get

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from yaml import load as load_yaml, Loader

from accounts.models import Shop
from category.models import Category, CategoryShop
from product.models import ProductInfo, Product, Parameter, ProductParameter, Img
from product.serializers import ProductSerializer, ProductInfoSerializer, ProductInfoINSerializer


class AddProducts(APIView):
    """Добавление продуктов до 3х

    {data:
        shop: id,
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
        price: product_price,
        quantity: product_quantity,
        img: img_path
        }]
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'Error': 'Login required'}, status=401)

        if user.type != 'shop':
            return JsonResponse({'Error': 'User\'s type "shop" only'}, status=401)

        shop_id = request.data.get('shop')
        if not shop_id and Shop.objects.get(id=shop_id).user.id != user.id:
            return JsonResponse({'Error': 'not existed parameter "shop" or you not owner this shop'},
                                status=401)

        products = request.data.get('products')

        if type(products) is list and len(products) < 4:
            response_dict = {'category': {
                                'create': [],
                                'no_crete': []},
                             'products': {
                                 'create': [],
                                 'no_crete': []
                             }}

            for product in products:
                product_serializer = ProductInfoSerializer(data=product)
                if not product_serializer.is_valid():
                    return JsonResponse({'Error': product_serializer.errors}, status=401)

                product_inform = product_serializer.initial_data
                product_item = product_inform.get('product')
                category_name = product_item.get('category')

                try:
                    category_object = Category.objects.get_or_create(name=category_name)
                except django.db.utils.IntegrityError:
                    return JsonResponse({'Error': 'try agen'})

                if category_object[1]:
                    response_dict.get('category').get('create').append(str(category_object[0]))
                else:
                    response_dict.get('category').get('no_crete').append(str(category_object[0]))
                CategoryShop.objects.get_or_create(category=category_object[0], shop_id=shop_id)

                product = Product.objects.get_or_create(name=product_item.get('name'),
                                                        category=category_object[0])
                if product[1]:
                    response_dict.get('products').get('create').append(str(product[0]))
                else:
                    response_dict.get('products').get('no_crete').append(str(product[0]))
                product_info = ProductInfo.objects.get_or_create(product=product[0],
                                                                 external_id=product_inform.get('external_id'),
                                                                 shop_id=shop_id,
                                                                 price=product_inform.get('price'),
                                                                 quantity=product_inform.get('quantity'))
                #  TODo добавить валидацию картинки.
                if product_inform.get('img'):
                    Img.objects.get_or_create(product_info=product_info[0],
                                              img=product_inform.get('img'))

                for product_parameter in product_inform.get('product_parameters'):
                    parameter_object = Parameter.objects.get_or_create(name=product_parameter.get('parameter'))

                    ProductParameter.objects.get_or_create(product_info=product_info[0],
                                                           parameter=parameter_object[0],
                                                           value=product_parameter.get('value'))

            return JsonResponse({'Msg': response_dict}, status=201)

        elif len(products) >= 4:
            JsonResponse({'msg': 'For add more then 4 products use method UpdateCatalog'}, status=401)
        else:
            JsonResponse({'Error': 'bad request'}, status=401)
        return JsonResponse({'ok': 'ok'})


class UpdateCatalog(APIView):

    """обновление католога
    """
    permission_classes = [IsAuthenticated]
    # TODO Уменьшить количество обращений к БД
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
                shop = Shop.objects.get_or_create(name=data.get('shop'),
                                                  user_id=request.user.id)
                for category in data.get('categories'):
                    category_object = Category.objects.get_or_create(id=category.get('id'),
                                                                     name=category.get('name'))
                    CategoryShop.objects.get_or_create(category=category_object[0],
                                                       shop=shop[0])
                ProductInfo.objects.filter(shop=shop[0]).delete()
                for item in data.get('goods'):
                    product = Product.objects.get_or_create(name=item.get('name'),
                                                            category_id=item.get('category'))
                    product_info = ProductInfo.objects.get_or_create(product=product[0],
                                                                     external_id=item.get('id'),
                                                                     shop=shop[0],
                                                                     price=item.get('price'),
                                                                     quantity=item.get('quantity'))
                    for name, value in item.get('parameters').items():
                        parameter_object = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(product_info=product_info[0],
                                                        parameter=parameter_object[0],
                                                        value=value)
                return JsonResponse({'Msg': 'all create'}, status=201)
        return JsonResponse({'Errors': 'Url error. Not specified basic arguments'})

#
# class ProductInfoView(APIView):
#     """
#     query_params:{
#         'shop_id': id,
#         'category_id': id
#         }
#     """
#     queryset = ProductInfo.objects.none()
#     permission_classes = [AllowAny]
#
#     def get(self, request, *args, **kwargs):
#
#         query = Q(shop__order_accepting=True)
#         shop_id = request.query_params.get('shop_id')
#         category_id = request.query_params.get('category_id')
#
#         if shop_id:
#             query = query & Q(shop_id=shop_id)
#
#         if category_id:
#             query = query & Q(product__category_id=category_id)
#
#         queryset = ProductInfo.objects.filter(query).\
#             select_related('product__category', 'shop').\
#             prefetch_related('product_parameters__parameter', 'img').\
#             distinct()
#
#         serializer = ProductInfoINSerializer(queryset, many=True)
#         return Response(serializer.data)


class ProductInfoViewSet(ViewSet):
    """
    query_params:{
        'shop_id': id,
        'category_id': id
        }
    """

    queryset = ProductInfo.objects.none()
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        query = Q(shop__order_accepting=True)
        shop_id = request.query_params.get('shop_id')
        category_id = request.query_params.get('category_id')

        if shop_id:
            query = query & Q(shop_id=shop_id)

        if category_id:
            query = query & Q(product__category_id=category_id)

        queryset = ProductInfo.objects.filter(query).\
            select_related('product__category', 'shop').\
            prefetch_related('product_parameters__parameter', 'img').\
            distinct()

        serializer = ProductInfoINSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            product = ProductInfo.objects.get(id=pk)
        except ObjectDoesNotExist as e:
            return JsonResponse({'Error': f'product with id {pk} - {e}'})
        serializer = ProductInfoINSerializer(product)
        return Response(serializer.data)


