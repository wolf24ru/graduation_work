from django.core.exceptions import ObjectDoesNotExist, FieldError
from drf_spectacular.utils import extend_schema
from ujson import loads

from django.http import JsonResponse
from django.db.models import Sum, F, Q
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from order.models import Order, OrderItem
from accounts.serializers import ResponseSerializer, ResponseErrorSerializer
from order.serializers import OrderSerializer, OrderItemSerializer, OrderItemAddQuantitySerializer,\
    BasketDeleteSerializer, BasketPutSerializer, CreateOrderSerializer

from order.tasks import new_order_email_task

from product.models import ProductInfo


class BasketViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    @extend_schema(
        responses={200: OrderSerializer,
                   400: ResponseErrorSerializer}
    )
    def list(self, request, *args, **kwargs):
        """Получение корзины"""
        try:
            basket = self.queryset.filter(user_id=request.user.id, status='basket'). \
                prefetch_related('order_items__product_info__product__category',
                                 'order_items__product_info__product_parameters__parameter'). \
                annotate(
                total_sum=Sum(F('order_items__quantity') * F('order_items__product_info__price'))). \
                distinct()
            p = self.queryset.filter
            serializer = OrderSerializer(basket, many=True)
            return Response(serializer.data)
        except FieldError:
            return JsonResponse({'Error': f'basket is empty.'})

    @extend_schema(
        request=OrderItemSerializer,
        responses={200: ResponseSerializer,
                   400: ResponseErrorSerializer}
    )
    def create(self, request, *args, **kwargs):
        """
        Создание корзины:
        """
        items = request.data.get('items')
        if items:
            basket = self.queryset.get_or_create(user_id=request.user.id,
                                                 status='basket')

            for item in items:
                product = ProductInfo.objects.filter(id=item['product_info']).select_related('product')[0]
                if product.quantity < item['quantity']:
                    return JsonResponse({'Error': f'For (id: {product.id}) - {product.product.name} exceeded quantity'})
                item.update({'order': basket[0].id})
                serializer = OrderItemSerializer(data=item)
                if serializer.is_valid():
                    try:
                        serializer.save()
                    except IntegrityError as e:
                        return JsonResponse({'Error': str(e)})
                else:
                    return JsonResponse({'Error': f'serializer error: {serializer.errors}'}, status=401)
            return JsonResponse({'Msg': 'items was added in basket'})
        return JsonResponse({'Error': 'incorrect arguments'})

    @extend_schema(
        request=BasketDeleteSerializer,
        responses={200: ResponseSerializer,
                   400: ResponseErrorSerializer}
    )
    def destroy(self, request, *args, **kwargs):
        """Удаление товаров из корзины
    items: [id_items]
    """
        items_id_list = request.data.get('items')
        if items_id_list:
            query = Q()
            try:
                basket = self.queryset.objects.get(user_id=request.user.id, status='basket')
            except ObjectDoesNotExist:
                return JsonResponse({'Msg': 'Basket is empty. Basket do not create yet'})
            else:
                for id_item in items_id_list:
                    if not type(id_item) == int:
                        id_digit = id_item.isdigit()
                    else:
                        id_digit = True
                    if id_digit:
                        query = query | Q(order=basket, id=id_item)
                if query:
                    delete_count = OrderItem.objects.filter(query).delete()[0]
                    return JsonResponse({'Msg': f'deleted {delete_count} items'})
            return JsonResponse({'Error': 'incorrect arguments'})

    @extend_schema(
        request=BasketPutSerializer,
        responses={200: ResponseSerializer,
                   400: ResponseErrorSerializer}
    )
    def update(self, request, *args, **kwargs):
        """Добавить количество товаров в корзину"""
        json_valid_error = {'Error': {
            'msg': 'Valid Error in items',
            'items': []
        }}

        json_valid = {
            'Msg': {
                'msg': 'objects update',
                'items': []
            }
        }

        items_list = request.data.get('items')
        if items_list:
            basket = self.queryset.objects.get_or_create(user_id=request.user.id,
                                                         status='basket')
            order_items_queryset = OrderItem.objects.filter(order=basket[0]).all()
            for _order_item in order_items_queryset:
                for order_item in items_list:
                    product = ProductInfo.objects.filter(id=order_item['product_info']).select_related('product')[0]
                    if product.quantity < order_item['quantity']:
                        return JsonResponse(
                            {'Error': f'For (id: {product.id}) - {product.product.name} exceeded quantity'})

                    serializer = OrderItemAddQuantitySerializer(data=order_item)
                    if serializer.is_valid():
                        if _order_item.id == order_item['id']:
                            _order_item.quantity = order_item['quantity']
                            json_valid['Msg']['items'].append(order_item)
                    else:
                        json_valid_error['Error']['items'].append(order_item)

            OrderItem.objects.bulk_update(order_items_queryset, ['quantity'])
            if json_valid['Msg']['items'] and json_valid_error['Error']['items']:
                return JsonResponse({json_valid,
                                     json_valid_error})
            elif json_valid_error['Error']['items']:
                return JsonResponse(json_valid_error)
            elif json_valid['Msg']['items']:
                return JsonResponse(json_valid)
            else:
                return JsonResponse({'Error': 'invalid request '})

                
class VendorOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: OrderSerializer,
                   400: ResponseErrorSerializer}
    )
    def get(self, request, *args, **kwargs):
        """Работа с заказами магазином"""
        if request.user.type != 'shop':
            return JsonResponse({'Error': 'Only for users with status "shop" '}, status=403)
        orders = Order.objects.filter(order_items__product_info__shop__user=request.user). \
            exclude(status='basket'). \
            prefetch_related('order_items__product_info__product__category',
                             'order_items__product_info__product_parameters__parameter'). \
            select_related('contact'). \
            annotate(total_sum=(Sum(F('order_items__quantity') * F('order_items__cost_one')))). \
            distinct()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    """Получение и создания заказов"""

    @extend_schema(
        responses={200: OrderSerializer,
                   400: ResponseErrorSerializer}
    )
    def get(self, request, *args, **kwargs):
        """Получить заказы"""
        order = Order.objects.filter(user_id=request.user.id).\
            exclude(status='basket').\
            prefetch_related('order_items__product_info__product__category',
                             'order_items__product_info__product_parameters__parameter').\
            select_related('contact').\
            annotate(total_sum=Sum(F('order_items__quantity') * F('order_items__cost_one')))\
            .distinct()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=CreateOrderSerializer,
        responses={200: ResponseSerializer,
                   400: ResponseErrorSerializer}
    )
    def post(self, request, *args, **kwargs):
        """Создать заказ(переместить из корзины на исполнение)
        """
        order_items_list = []
        quantity_error_list = []
        contact = request.data.get('contact')
        if contact:
            if not type(contact) == int:
                id_digit = contact.isdigit()
            else:
                id_digit = True
            if id_digit:
                try:
                    order = Order.objects.filter(user_id=request.user.id,
                                                 status='basket').distinct()
                    if order:
                        order_items = OrderItem.objects.filter(order=order[0]). \
                            prefetch_related('product_info')

                        for item in order_items:
                            if item.product_info.quantity < item.quantity:
                                quantity_error_list.append(item.id)
                                continue
                            ProductInfo.objects.filter(id=item.product_info.id). \
                                update(quantity=F('quantity') - item.quantity)
                            item.cost_one = item.product_info.price
                            order_items_list.append(item)
                    order_update = order.update(contact_id=request.data['contact'],
                                                status='new')
                except IntegrityError as e:
                    return JsonResponse({'Error': str(e)})
                else:
                    if order_update:
                        update_cost = OrderItem.objects.bulk_update(order_items_list, ['cost_one'])
                        new_order_email_task.delay(user_id=request.user.id)
                        # new_order.send(sender=self.__class__, user_id=request.user.id)
                        if quantity_error_list:
                            return JsonResponse(
                                {
                                    'Msg': 'create new orders',
                                    'Warning': f'in products (id: {quantity_error_list}) exceeded quantity'
                                })
                        return JsonResponse({'Msg': 'create new orders'})
                    else:
                        return JsonResponse({'Msg': 'basket is empty'})
        return JsonResponse({'Error': 'incorrect arguments'})


