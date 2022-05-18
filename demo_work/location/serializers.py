from rest_framework import serializers

from location.models import RegionCity, Region, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'city')
        read_only_fields = ('id', 'city')


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'region')
        read_only_fields = ('id', 'region')

class RegionCitySerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    city = CitySerializer()

    class Meta:
        model = RegionCity
        fields = ('id', 'region', 'city')
        read_only_fields = ('id', 'region', 'city')
