from rest_framework import serializers

from accounts.models import CustomUser, Contact, Shop


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'user', 'region', 'city',
                  'street', 'house', 'structure',
                  'building', 'apartment', 'phone_validator')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name',
                  'email', 'company', 'position',
                  'username', 'contacts')
        read_only_fields = ('id',)
