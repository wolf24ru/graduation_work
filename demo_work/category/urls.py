
from category.views_api import CategoryView
from django.urls import path

urlpatterns = [
    path('category/', CategoryView.as_view(), name='category'),
]
