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


class ResponseUserFilling(serializers.Serializer):
    Status = serializers.BooleanField(default=True)

    class Meta:
        fields = ('Status',)


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


class ContactPutSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Contact
        fields = ('id', 'region', 'city',
                  'street', 'house', 'structure',
                  'building', 'apartment', 'phone_number')


class ResponseSerializer(serializers.Serializer):
    Msg = serializers.StringRelatedField(default='Text response message')

    class Meta:
        fields = ('Msg',)


class ResponseErrorSerializer(serializers.Serializer):
    Error = serializers.StringRelatedField(default='Error message')

    class Meta:
        fields = ('Error',)


class RespoonseNewTokenSerializer(serializers.Serializer):
    user = serializers.StringRelatedField(default='user parameter')
    new_token = serializers.StringRelatedField(default='Token')

    class Meta:
        fields = ('user', 'new_token')
