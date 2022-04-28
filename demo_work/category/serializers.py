from rest_framework import serializers

from category.models import Category, CategoryShop


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)

# class CategoryShopSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = CategoryShop
#         fields = ('id')
#         read_only_fields = ('id',)
