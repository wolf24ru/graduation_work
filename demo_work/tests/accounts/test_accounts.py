from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from rest_framework import status


from rest_framework.test import APIClient


def test_something():
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
    url += reverse('registration')
    response = client.post(url, json_data, format='json')
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_get_user_filling(client, url, user_factory, get_token_url, token):
    token = token()
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
def test_post_user_filling(client, url, get_token_url, token, json_data, expected_status):
    token = token()
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
def test_get_vendor_status(url, token, shop, client, _type, expected_status):
    _token = token(user__type=_type)
    shop(user=_token.user)
    url += reverse('order_accepting')
    client.credentials(HTTP_AUTHORIZATION='Token ' + _token.key)
    response = client.get(url)
    assert response.status_code == expected_status
    # assert response.data.get('order_accepting')


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
def test_post_vendor_status(url, token, shop, client, _type, expected_status):
    _token = token(user__type=_type)
    _shop = shop(user=_token.user)
    url += reverse('order_accepting')
    client.credentials(HTTP_AUTHORIZATION='Token ' + _token.key)

    order_accepting = not _shop.order_accepting
    json_data = {'order_accepting':  order_accepting}
    response = client.post(url, json_data, format='json')
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_get_сontact(client, token, contact, url):
    url += reverse('contacts')
    _token = token()
    _contact = contact(user=_token.user, phone_number='+79939052000')
    client.credentials(HTTP_AUTHORIZATION='Token ' + _token.key)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

# TODO написать тест
@pytest.mark.django_db
def test_post_сontact(client, token, url):
    url += reverse('contacts')
    _token = token()

    client.credentials(HTTP_AUTHORIZATION='Token ' + _token.key)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK