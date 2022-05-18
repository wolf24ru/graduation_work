from django.db import models
from django.utils.translation import gettext_lazy as _
from product.models import ProductInfo
from accounts.models import CustomUser, Contact

STATUS_ORDER = (
    ('basket', 'В корзине'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Сборка'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)


class Order(models.Model):
    user = models.ForeignKey(CustomUser,
                             verbose_name=_('User'),
                             related_name='orders',
                             blank=True,
                             on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(_('status'),
                              choices=STATUS_ORDER,
                              max_length=15,
                              help_text=_('Shows the order status'))
    contact = models.ForeignKey(Contact,
                                verbose_name=_('Contact'),
                                related_name='orders',
                                blank=True,
                                null=True,
                                on_delete=models.CASCADE)


    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('List orders')
        ordering = ('-date',)

    def __str__(self):
        return str(self.date)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              verbose_name=_('Order Item'),
                              related_name='order_items',
                              blank=True,
                              on_delete=models.CASCADE)
    product_info = models.ForeignKey(ProductInfo,
                                     verbose_name=_('product info'),
                                     related_name='order_items',
                                     blank=True,
                                     on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('quantity'))
    cost_one = models.FloatField(_('cost'),
                                 help_text='cost for one position',
                                 blank=True,
                                 null=True)

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('List orders items')
        constraints = [
            models.UniqueConstraint(fields=['order', 'product_info'], name='unique_order_item'),
        ]


class OrderCost(models.Model):
    order = models.ForeignKey(Order,
                              verbose_name=_('Order'),
                              related_name='order_cost',
                              blank=True,
                              on_delete=models.CASCADE
                              )
    delivery_cost = models.PositiveIntegerField(_('Delivery cost'))
    items_cost = models.PositiveIntegerField(_('Items cost'))

    class Meta:
        verbose_name = _('Order cost')
        verbose_name_plural = _('List of orders cost')
