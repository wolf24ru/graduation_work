from django.db import models
from category.models import Category
from accounts.models import Shop
from django.utils.translation import gettext_lazy as _


class Parameter(models.Model):
    name = models.CharField(_('parameter\'s name'), max_length=58)

    class Meta:
        verbose_name = _('Product\'s info')
        verbose_name_plural = _('List product\'s info')
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,
                                 verbose_name=_('Category'),
                                 related_name='products',
                                 blank=True,
                                 on_delete=models.CASCADE
                                 )
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('list products')
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    # model
    external_id = models.PositiveIntegerField(_('External ID'))
    product = models.ForeignKey(Product,
                                verbose_name=_('Product'),
                                related_name='product_infos',
                                blank=True,
                                on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop,
                             verbose_name=_('Shop'),
                             related_name='product_info',
                             blank=True,
                             on_delete=models.CASCADE)
    price = models.PositiveIntegerField(_('Price'),)
    quantity = models.PositiveIntegerField(_('Quantity'))

    class Meta:
        verbose_name = _('Info about product')
        verbose_name_plural = _('Information list about products')
        constraints = [
            models.UniqueConstraint(fields=['product', 'shop', 'external_id'], name='unique_product_info'),
         ]


class Img(models.Model):
    product_info = models.ForeignKey(ProductInfo,
                                     verbose_name=_('product\'s info'),
                                     related_name='img',
                                     on_delete=models.CASCADE)
    img = models.ImageField(verbose_name=_('Image'))


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo,
                                     verbose_name=_('product\'s info'),
                                     related_name='product_parameters',
                                     blank=True,
                                     on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter,
                                   verbose_name=_('product\'s parameter'),
                                   related_name='product_parameter',
                                   blank=True,
                                   on_delete=models.CASCADE)
    value = models.CharField(_('value'), max_length=50)
