from distutils.util import strtobool

from django.db.models import Q
from location.models import RegionCity
from accounts.models import Shop, CustomUser, Contact
from accounts.validator import phon_valid
from django.contrib.auth.password_validation import validate_password
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from accounts.serializers import UserSerializer, ShopSerializer, ContactSerializer, GetContactSerializer
from rest_framework.authtoken.models import Token


from django.http import JsonResponse


class RegistrationUser(APIView):
    """Регистрация пользователя"""
    queryset = CustomUser.objects.none()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        _argument_dict = {'first_name', 'last_name', 'email',
                          'password', 'company', 'position', 'username', 'type'}
        _required_argument = {'password', 'email', 'company'}
        data_in_set = set(request.data)
        if data_in_set.issubset(_argument_dict):
            if _required_argument.issubset(data_in_set):
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
                return JsonResponse({'Error': 'entered  do not full list of argument'})
        else:
            return JsonResponse({'Error': 'unexpected argument'})


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


class VendorStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Получить текущий статус поставщика"""
        if request.user.type != 'shop':
            return JsonResponse({'Error': 'Only for users with status "shop" '}, status=403)
        vendor = request.user.shop
        serializer = ShopSerializer(vendor)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Изменить статус магазина"""
        if request.user.type != 'shop':
            return JsonResponse({'Error': 'Only for users with status "shop" '}, status=403)
        order_accepting = request.data.get('order_accepting')
        if order_accepting:
            try:
                Shop.objects.filter(user_id=request.user.id).\
                    update(order_accepting=strtobool(order_accepting))
                return JsonResponse({'Msg': f'order accepting changed to {order_accepting}'})
            except ValueError as e:
                return JsonResponse({'Error': str(e)})
        return JsonResponse({'Error': 'unexpected argument'}, status=401)


class ContactView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Получить контакты пользователя"""
        contact = Contact.objects.filter(user_id=request.user.id)
        serializer = GetContactSerializer(contact, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Добавление контакта"""
        if {'region', 'city', 'street', 'phone_number'}.issubset(request.data):
            city = request.data.get('city').capitalize()
            region = request.data.get('region').capitalize()
            region_city = RegionCity.objects.filter(city__city=city,
                                                    region__region=region).first()
            if region_city:
                # request.data._mutable = True
                phone_number = phon_valid(request.data['phone_number'])
                if not phone_number:
                    return JsonResponse({'Msg': f'your phone number do not correct: {request.data["phone_number"]}.'
                                                f' Try like +7 (999) 999-99-99'})
                request.data.update({'user': request.user.id})
                request.data['region'] = region_city.region.id
                request.data['city'] = region_city.city.id
                request.data['phone_number'] = phone_number
                serializer = ContactSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'Msg': 'Contact create'}, status=201)
                else:
                    return JsonResponse({'Error': serializer.errors}, status=401)
            else:
                return JsonResponse({'Error': 'City and region do not correlate.'
                                              'Try to watch your region or city in list'
                                              'Use api/v1/location/location_inform'}, status=401)

        return JsonResponse({'Error': 'unexpected argument'}, status=401)

    def delete(self, request, *args, **kwargs):
        """Удаленее контакта
        {"contacts_id":[ids]}
        """
        contacts_id_list = request.data.get('contacts_id')
        if contacts_id_list:
            query = Q()
            for contact_id in contacts_id_list:
                if type(contact_id) == int:
                    query = query | Q(user_id=request.user.id, id=contact_id)
                elif contact_id.isdigit():
                    query = query | Q(user_id=request.user.id, id=contact_id)
            if query:
                deleted_count = Contact.objects.filter(query).delete()[0]
                return JsonResponse({'Msg': f'Delete {deleted_count} contacts'})
        return JsonResponse({'Error': 'unexpected argument'}, status=401)

    def put(self, request, *args, **kwargs):
        """Редактирование контакта
        {
        "id":
        }
        """
        if 'id' in request.data:
            id_digit = bool
            if not type(request.data['id']) == int:
                id_digit = request.data['id'].isdigit()
            else:
                id_digit = True

            if id_digit:
                contact = Contact.objects.filter(id=request.data['id'],
                                                 user_id=request.user.id).first()
                if {'region', 'city'}.issubset(request.data):
                    city = request.data.get('city').capitalize()
                    region = request.data.get('region').capitalize()
                    region_city = RegionCity.objects.filter(city__city=city,
                                                            region__region=region).first()
                    if region_city:
                        request.data['region'] = region_city.region.id
                        request.data['city'] = region_city.city.id
                    else:
                        return JsonResponse({'Error': 'City and region do not correlate.'
                                                      'Try to watch your region or city in list'
                                                      'Use api/v1/location/location_inform'}, status=401)
                if {'phone_number'}.issubset(request.data):
                    phone_number = phon_valid(request.data['phone_number'])
                    if not phone_number:
                        return JsonResponse({'Msg': f'your phone number do not correct: {request.data["phone_number"]}.'
                                                    f' Try like +7 (999) 999-99-99'})
                    request.data['phone_number'] = phone_number
                if contact:
                    serializer = ContactSerializer(contact,
                                                   data=request.data,
                                                   partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'Msg': 'Contact was changed'})
                    else:
                        return JsonResponse({'Error': serializer.errors})

        return JsonResponse({'Error': 'unexpected argument'}, status=401)


class NewToken(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        tk = Token.objects.filter(user_id=request.user.id).distinct()
        token = tk[0].generate_key()
        tk.update(key=token)

        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'new_token': token
        }
        return JsonResponse(content)