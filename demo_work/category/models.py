from django.db import models
from django.utils.translation import gettext_lazy as _
from demo_work.accounts.models import Shop


class Category(models.Model):
    name = models.CharField(_('Category\'s name'), max_length=58)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('List category')
        ordering = ('-name',)

    def __str__(self):
        return self.name


class CategoryShop(models.Model):
    category = models.ForeignKey(Category,
                                 verbose_name=_('Category'),
                                 related_name='category_shops',
                                 on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop,
                             verbose_name=_('Shop'),
                             related_name='category_shops',
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ('-shop',)
        constraints = [
            models.UniqueConstraint(fields=['shop', 'category'],
                                    name='unique_category_info'),
        ]
