from django.utils.translation import gettext_lazy as _
from django.db import models


class Region(models.Model):
    region = models.CharField(_('region'), max_length=150)

    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Region\'s list')

    def __str__(self):
        return f'{self.region}'


class City(models.Model):
    city = models.CharField(_('city'), max_length=100)

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('City\'s list')

    def __str__(self):
        return f'{self.city}'


class RegionCity(models.Model):
    region = models.ForeignKey(Region,
                               verbose_name=_('Region'),
                               related_name='region_rc',
                               on_delete=models.CASCADE)
    city = models.ForeignKey(City,
                             verbose_name=_('City'),
                             related_name='city_rc',
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.region}: {self.city}'
