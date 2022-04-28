from rest_framework.generics import ListAPIView
from category.models import Category

from category.serializers import CategorySerializer


class CategoryView(ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
