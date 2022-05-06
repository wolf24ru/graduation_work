from rest_framework import serializers

from accounts.models import CustomUser, Contact, Shop

from location.serializers import CitySerializer, RegionSerializer


class ContactSerializer(serializers.ModelSerializer):


    class Meta:
        model = Contact
        fields = ('id', 'user', 'region', 'city',
                  'street', 'house', 'structure',
                  'building', 'apartment', 'phone_number')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }


class GetContactSerializer(ContactSerializer):
    region = RegionSerializer()
    city = CitySerializer()

class UserSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name',
                  'email', 'company', 'position',
                  'username', 'contacts', 'type')
        read_only_fields = ('id',)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'order_accepting')
        read_only_fields = ('id',)
