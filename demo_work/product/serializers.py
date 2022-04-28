from rest_framework import serializers
from product.models import Parameter, Product, ProductInfo, ProductParameter, Img


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value')


class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img()
        fields = ('id', 'img',)
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'category')
        read_only_fields = ('id',)


class ProductInfoSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField(required=False)
    product = ProductSerializer(required=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'img', 'product', 'product_parameters', 'price', 'shop', 'quantity')
        read_only_fields = ('id',)







