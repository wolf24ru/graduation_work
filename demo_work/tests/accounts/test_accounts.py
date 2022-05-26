import base64
import pytest
from django.urls import reverse
from rest_framework import status
import ast


def test_something():
    """Проверка работы тестов"""
    assert True


@pytest.mark.parametrize(
    ['json_data', 'expected_status'],
    (
            (
                    {
                        'email': 'email@mail.ru',
                        'password': '12345678qwerty',
                        'company': 'ООО "ППР"',
                        'position': 'manager',
                        'username': 'pupkin'
                    }, status.HTTP_201_CREATED
            ),
            (
                    {
                        'email': 'ejhmail@mail.ru',
                        'company': 'ООО "ППР"',
                        'position': 'manager',
                        'username': 'pupkin'
                    }, status.HTTP_400_BAD_REQUEST
            ),
            (
                    {
                        'password': '12345678qwerty',
                        'company': 'ООО "ППР"',
                        'position': 'manager',
                        'username': 'pupkin'
                    }, status.HTTP_400_BAD_REQUEST
            ),
            (
                    {
                        'company': 'ООО "ППР"',
                        'position': 'manager',
                        'username': 'pupkin'
                    }, status.HTTP_400_BAD_REQUEST
            ),
            (
                    {
                        'email': 'email@mail.ru',
                        'password': '12345678qwerty',
                    }, status.HTTP_400_BAD_REQUEST
            ),
    )
)
@pytest.mark.django_db
def test_create_account(client, json_data, expected_status, url):
    """Создание аккаунта"""
    url += reverse('registration')
    response = client.post(url, json_data, format='json')
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_get_user_filling(client, url, user_factory, get_token_url, token_factory):
    """Получение информации о пользователи"""
    token = token_factory()
    url += reverse('user_filling')
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = client.get(url)
    print(response)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('email') == token.user.email


@pytest.mark.parametrize(
    ['json_data', 'expected_status'],
    (
            (
                    {
                        'email': 'email@mail.ru',
                    }, status.HTTP_200_OK
            ),
            (
                    {
                        'company': 'ООО "ППР"',
                    }, status.HTTP_200_OK
            ),
            (
                    {
                        'password': '12345678qwerty',
                    }, status.HTTP_200_OK
            ),
            (
                    {
                        'position': 'manager',
                        'username': 'pupkin'
                    }, status.HTTP_200_OK
            )
    )
)
@pytest.mark.django_db
def test_post_user_filling(client, url, get_token_url, token_factory, json_data, expected_status):
    """Изменение информации пользователя"""
    token = token_factory()
    url += reverse('user_filling')
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(url, json_data, format='json')
    assert response.status_code == expected_status


@pytest.mark.parametrize(('_type', 'expected_status'),
                         (
                                 (
                                     'shop',
                                     status.HTTP_200_OK
                                 ),
                                 (
                                     'buyer',
                                     status.HTTP_403_FORBIDDEN
                                 )
                         )
                         )
@pytest.mark.django_db
def test_get_vendor_status(url, token_factory, shop_factory, client, _type, expected_status):
    """Получение статуса магазина"""
    _token = token_factory(user__type=_type)
    shop_factory(user=_token.user)
    url += reverse('order_accepting')
    client.credentials(HTTP_AUTHORIZATION='Token ' + _token.key)
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(('_type', 'expected_status'),
                         (
                                 (
                                     'shop',
                                     status.HTTP_200_OK
                                 ),
                                 (
                                     'buyer',
                                     status.HTTP_403_FORBIDDEN
                                 )
                         )
                         )
@pytest.mark.django_db
def test_post_vendor_status(url, token_factory, shop_factory, client, _type, expected_status):
    """Изменение статуса магазина"""
    _token = token_factory(user__type=_type)
    _shop = shop_factory(user=_token.user)
    url += reverse('order_accepting')
    client.credentials(HTTP_AUTHORIZATION='Token ' + _token.key)

    order_accepting = not _shop.order_accepting
    json_data = {'order_accepting':  order_accepting}
    response = client.post(url, json_data, format='json')
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_get_contact(client, token_factory, contact_factory, url):
    """Получение контактов пользователя"""
    url += reverse('contacts')
    _token = token_factory()
    _contact = contact_factory(user=_token.user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + _token.key)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    ['json_data', 'expected_status'],
    ((
             {
                 "region": 1,
                 "city": 1,
                 "street": "Павлова",
                 "house": "152",
                 "apartment": "415",
                 "phone_number": "+79546152012"
             }, status.HTTP_201_CREATED
     ),
     (
             {
                 "region": 0,
                 "city": 1,
                 "street": "Павлова",
                 "house": "152",
                 "apartment": "415",
                 "phone_number": "+79546152012"
             }, status.HTTP_400_BAD_REQUEST
     ),
     (
             {
                 "region": 1,
                 "city": 0,
                 "street": "Павлова",
                 "house": "152",
                 "apartment": "415",
                 "phone_number": "+79546152012"
             }, status.HTTP_400_BAD_REQUEST
     ),
     (
             {
                 "region": 1,
                 "city": 1
             }, status.HTTP_400_BAD_REQUEST
     ),
     (
             {
                 "region": 1,
                 "city": 1,
                 "street": "Павлова",
                 "phone_number": "+79546152012"
             }, status.HTTP_201_CREATED
     ),
     (
             {
                 "region": 1,
                 "city": 1,
                 "street": "Павлова",
                 "house": "152",
                 "structure": "dsf",
                 "building": "4dc",
                 "apartment": "415",
                 "phone_number": "+79546152012"
             }, status.HTTP_201_CREATED
     ),
     (
             {
                 "region": 1,
                 "city": 1,
                 "street": "Павлова",
                 "house": "152",
                 "structure": "dsf",
                 "building": "4dc",
                 "apartment": "415",
                 "phone_number": "000"
             }, status.HTTP_400_BAD_REQUEST
     ),
     (
             {
                 "region": 1,
                 "city": 1,
                 "street": "Павлова",
                 "house": "152",
                 "structure": "dsf",
                 "building": "4dc",
                 "apartment": "415",
                 "phone_number": "89546152012"
             }, status.HTTP_201_CREATED
     ),
     (
             {"": ""}, status.HTTP_400_BAD_REQUEST
     ),
     (
             {
                 "street": "Павлова",
                 "house": "152",
                 "structure": "dsf",
                 "building": "4dc",
                 "apartment": "415",
                 "phone_number": "89546152012"
             }, status.HTTP_400_BAD_REQUEST
     ),
    )
)
@pytest.mark.django_db
def test_post_contact(client, token_factory, url, json_data, region_city_factory, expected_status):
    """Добавление контакта пользователя"""
    url += reverse('contacts')
    _token = token_factory()
    _rc = region_city_factory(_quantity=3)
    region = json_data.get('region')
    city = json_data.get('city')

    match region:
        case 1:
            json_data.update({'region': _rc[1].region.region})
        case 0:
            json_data.update({'region': _rc[0].region.region})
    match city:
        case 1:
            json_data.update({'city': _rc[1].city.city})
        case 0:
            json_data.update({'city': _rc[0].city.city})

    client.credentials(HTTP_AUTHORIZATION='Token ' + _token.key)
    response = client.post(url, json_data, format='json')
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_delete_contact(client, token_factory, contact_factory, url):
    """Удаление контакта пользователя"""
    url += reverse('contacts')
    _token = token_factory()
    _contact = contact_factory(user=_token.user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + _token.key)
    response = client.delete(url, {'contacts_id': [_contact.id]})
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.parametrize(
    ['json_data', 'expected_status'],
    (
            (
                    {
                        "id": 1,
                        "region": 1,
                        "city": 1,
                        "street": "gshfg",
                        "house": "541",
                        "structure": "fgdfg21",
                        "building": "dfg884",
                        "apartment": "62",
                        "phone_number": "89546152012"
                    }, status.HTTP_200_OK
            ),
            (
                    {
                        "region": 1,
                        "city": 1,
                        "street": "gshfg",
                        "house": "541",
                        "structure": "fgdfg21",
                        "building": "dfg884",
                        "apartment": "62",
                        "phone_number": "89546152012"
                    }, status.HTTP_400_BAD_REQUEST
            ),
            (
                    {
                        "id": 2,
                        "region": 1,
                        "city": 1,
                        "street": "gshfg",
                        "house": "541",
                        "structure": "fgdfg21",
                        "building": "dfg884",
                        "apartment": "62",
                        "phone_number": "89546152012"
                    }, status.HTTP_400_BAD_REQUEST
            ),
            (
                    {
                        "id": 1,
                        "region": 0,
                        "city": 1,
                        "street": "gshfg",
                        "house": "541",
                        "structure": "fgdfg21",
                        "building": "dfg884",
                        "apartment": "62",
                        "phone_number": "89546152012"
                    }, status.HTTP_400_BAD_REQUEST
            ),
            (
                    {
                        "id": 1,
                        "region": 1,
                        "city": 1,
                        "street": "gshfg",
                        "house": "541",
                        "structure": "fgdfg21",
                        "building": "dfg884",
                        "apartment": "62",
                        "phone_number": "0005"
                    }, status.HTTP_400_BAD_REQUEST
            ),
    )
)
@pytest.mark.django_db
def test_put_contact(client, token_factory, contact_factory, url, region_city_factory, json_data, expected_status):
    """Изменение контакта пользователя"""
    url += reverse('contacts')
    _token = token_factory()
    _rc = region_city_factory(_quantity=3)
    _contact = contact_factory(user=_token.user, region=_rc[0].region, city=_rc[0].city)
    region = json_data.get('region')
    city = json_data.get('city')
    match region:
        case 1:
            json_data.update({'region': _rc[1].region.region})
        case 0:
            json_data.update({'region': _rc[2].region.region})
    match city:
        case 1:
            json_data.update({'city': _rc[1].city.city})
        case 0:
            json_data.update({'city': _rc[2].city.city})
    if json_data.get('id'):
        match json_data.get('id'):
            case 1:
                json_data.update({'id': _contact.id})
            case 2:
                json_data.update({'id': 'not_digit'})

    client.credentials(HTTP_AUTHORIZATION='Token ' + _token.key)
    response = client.put(url, json_data, format='json')
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_new_token(client, url):
    """ПОлучение новго токена"""
    # регистарция полльзователя
    email = 'email@mail.ru'
    password = 'qwertygh12345'
    json_data = {
        'email': email,
        'password': password,
        'company': 'ООО "ППР"',
        'position': 'manager',
        'username': 'pupkin'
    }
    _url = url + reverse('registration')
    re = client.post(_url, json_data, format='json')
    # получение токена

    url_token = url + '/api-token-auth/'
    token = client.post(url_token, {"username": email,
                                    "password": password}).data['token']

    url += reverse('new_token')
    b64Val = base64.b64encode(f'{email}:{password}'.encode())
    client.credentials(HTTP_AUTHORIZATION='Basic ' + b64Val.decode())
    response = client.post(url, format='json')
    content = response.content
    new_token = ast.literal_eval(content.decode('utf-8')).get('new_token')

    assert response.status_code == status.HTTP_200_OK
    assert new_token != token
