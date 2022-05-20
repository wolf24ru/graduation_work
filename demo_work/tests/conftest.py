import random
import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from rest_framework.authtoken.models import Token


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def url():
    return 'http://localhost:8000'


@pytest.fixture
def get_token_url():
    return'http://localhost:8000/api-token-auth/'


def get_random_company():
    return random.choice(['ООО "Принцы"', 'ОА "Побег"', 'Листочек'])


def region_city():
    return random.choice(baker.make('RegionCity', _quantity=5))


def get_random_user_type():
    return random.choice(['shop', 'buyer'])


@pytest.fixture
def user_factory():
    def factory(**kwargs):

        return baker.make('CustomUser',
                          company=get_random_company(),
                          type=get_random_user_type(),
                          **kwargs)
    return factory


@pytest.fixture
def token():
    def factory(**kwargs):

        if kwargs.get('user__type'):
            return baker.make(Token,
                              user__company=get_random_company(),
                              user__type=kwargs.get('user__type'))
        return baker.make(Token,
                          user__company=get_random_company(),
                          user__type=get_random_user_type(),
                          )
    return factory


@pytest.fixture
def shop():
    def factory(**kwargs):
        return baker.make('Shop',
                          **kwargs)
    return factory


@pytest.fixture
def contact():
    def factory(**kwargs):
        reg_city = region_city()
        return baker.make('Contact',
                          region=reg_city.region,
                          city=reg_city.city,
                          **kwargs)
    return factory


