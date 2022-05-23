import itertools
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


def random_region_city():
    return random.choice(baker.make('RegionCity', _quantity=5))


def get_random_user_type():
    return random.choice(['shop', 'buyer'])


@pytest.fixture
def region_city_factory():
    def factory(**kwargs):
        region = ('Регион1', 'Регион2', 'Регион3')
        city = ('Город1', 'Город2', 'Город3')
        return baker.make('RegionCity',
                          region__region=itertools.cycle(region),
                          city__city=itertools.cycle(city),
                          **kwargs)
    return factory


@pytest.fixture
def user_factory():
    def factory(**kwargs):
        return baker.make('CustomUser',
                          company=get_random_company(),
                          type=get_random_user_type(),
                          **kwargs)
    return factory


@pytest.fixture
def token_factory():
    def factory(**kwargs):

        if kwargs.get('user__type'):
            return baker.make(Token,
                              user__company=get_random_company(),
                              **kwargs)
        return baker.make(Token,
                          user__company=get_random_company(),
                          user__type=get_random_user_type(),
                          **kwargs
                          )
    return factory


@pytest.fixture
def shop_factory():
    def factory(**kwargs):
        return baker.make('Shop',
                          **kwargs)
    return factory


@pytest.fixture
def contact_factory():
    def factory(**kwargs):
        if kwargs.get('region') and kwargs.get('city'):
            return baker.make('Contact', **kwargs)
        reg_city = random_region_city()
        return baker.make('Contact',
                          region=reg_city.region,
                          city=reg_city.city,
                          **kwargs)
    return factory


