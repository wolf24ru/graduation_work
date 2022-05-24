from rest_framework import serializers
from product.models import Parameter, Product, ProductInfo, ProductParameter, Img


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.CharField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value')


class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img()
        fields = ('img',)
        read_only_fields = ('img',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'category')
        read_only_fields = ('id',)


class ProductInfoSerializer(serializers.ModelSerializer):
    img = serializers.CharField(required=False)
    product = ProductSerializer(required=True)
    product_parameters = ProductParameterSerializer(many=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'product', 'price', 'shop', 'quantity', 'img', 'product_parameters', 'external_id')
        read_only_fields = ('id',)


class ProductInfoINSerializer(serializers.ModelSerializer):
    img = ImgSerializer(required=False, many=True)
    product = ProductSerializer(required=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'external_id', 'product', 'price', 'shop', 'quantity', 'img', 'product_parameters')
        read_only_fields = ('id',)



class ProductAddSerializer(serializers.Serializer):
    shop = serializers.CharField(default='shop_id')
    products = ProductInfoSerializer(many=True)


class ProductUpdateCatalogSerializer(serializers.Serializer):
    url = serializers.URLField()


class QueryParams(serializers.Serializer):
    shop_id = serializers.CharField(default="1", required=False)
    category_id = serializers.CharField(default="4", required=False)


class ProductListSerializer(serializers.Serializer):
    query_params = QueryParams()
