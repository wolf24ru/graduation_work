from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Shop, CustomUser, Contact
# Create your tests here.

class AccountTests(APITestCase):
    def test_create_account(self):
        url = reverse('registration')
        data = {
            'email': 'email@mail.ru',
            'password': '12345678qwerty',
            'company': 'ООО "ППР"',
            'position': 'manager',
            'username': 'pupkin'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.get().email, 'email@mail.ru')

    # def test_
