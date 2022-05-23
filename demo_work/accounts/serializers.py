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


class UserSerializerSchem(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name',
                  'email', 'password', 'company', 'position',
                  'username', 'contacts', 'type')
        read_only_fields = ('id',)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'order_accepting')
        read_only_fields = ('id',)


class ResponseRegistrSchem(serializers.Serializer):
    Msg = serializers.StringRelatedField(default='User successful create')

    class Meta:
        fields = ('Msg',)


class ResponseUserFilling(serializers.Serializer):
    Status = serializers.BooleanField(default=True)

    class Meta:
        fields = ('Status',)


class ResponseVendorStatus(serializers.Serializer):
    Msg = serializers.StringRelatedField(default='Order accepting changed to True')

    class Meta:
        fields = ('Msg',)


class ResponseContactDelete(serializers.Serializer):
    Msg = serializers.StringRelatedField(default='Delete 5 contacts')

    class Meta:
        fields = ('Msg',)


class ResponseContact(serializers.Serializer):
    Msg = serializers.StringRelatedField(default='Contact create')

    class Meta:
        fields = ('Msg',)


class RequestContactDelete(serializers.Serializer):
    order_accepting = serializers.BooleanField()

    class Meta:
        fields = ('Status',)


class RequestVendorStatus(serializers.Serializer):
    order_accepting = serializers.BooleanField()

    class Meta:
        fields = ('order_accepting',)
