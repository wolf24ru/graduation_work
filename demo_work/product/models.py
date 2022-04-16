from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.TextField()
