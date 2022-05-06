from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from location.models import City, Region

TYPE_USER = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """
        Создание пользователя
        :param email: email
        :param password: пароль
        :param kwargs: дополнительные значения
        :return: user
        """
        if not email:
            raise ValueError('Email is not set. Please set email')
        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.is_staff = False
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        """
        Создание супер пользователя
        :param email: email
        :param password: пароль
        :param kwargs: дополнительные значения
        :return: user
        """
        user = self.create_user(
            email=email,
            password=password,
            **kwargs
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    """
    Класс пользователя.

    email: email
    password: пороль
    company: Наименование компании
    position: Должность в компании
    username: Имя пользователя
    is_active: Рабочая учетная запись
    is_admin: Администратор
    type: Тип пользователя
    """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    email = models.EmailField(_('Email adres'), unique=True)
    company = models.CharField(_('Company'), max_length=100, blank=True)
    position = models.CharField(_('position'), max_length=100, blank=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('user name'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with this name already exist'),
        }
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_('Indicates that the user can use the account'
                    'Unselect this instead of deleting accounts'
                    ),
        )
    is_admin = models.BooleanField(
        _('Admin'),
        default=False,
        help_text=_('Indicates that the user is superuser'),
    )
    type = models.CharField(
        _('user type'),
        choices=TYPE_USER,
        max_length=5,
        default='buyer',
        help_text=_('choose your role in  between   shop and buyer'),
    )

    def __str__(self):
        return f'{self.username} {self.company} {self.type}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Список пользователей'
        ordering = ('email',)


class Contact(models.Model):
    """
        Контакты пользвоателя

        region: Регион
        city: Город
        street: улица
        house: дом
        structure: Корпус
        building: здание
        apartment: квартира или офис
        phone_validator: номер телефона
    """

    user = models.ForeignKey(CustomUser, verbose_name=_('User'),
                             related_name='contacts', blank=True,
                             on_delete=models.CASCADE)
    # country = models.CharField('Страна', max_length=58, blank=True)
    region = models.ForeignKey(Region,
                               verbose_name=_('Region'),
                               related_name='contacts',
                               on_delete=models.CASCADE)
    city = models.ForeignKey(City,
                             verbose_name=_('City'),
                             related_name='contacts',
                             on_delete=models.CASCADE)
    street = models.CharField(_('Street'), max_length=100)
    house = models.CharField(_('House'), max_length=15, blank=True)
    structure = models.CharField('Корпус', max_length=10, blank=True)
    building = models.CharField(_('building'), max_length=10, blank=True)
    apartment = models.CharField('Кв/Оф', max_length=10, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=20)

    class Meta:
        verbose_name = _('user contacts')
        verbose_name_plural = _('list of user contacts')


class Shop(models.Model):
    """
    Магазин

    url: сайт магазина
    name: название магазина
    user: пользователь(администратор) закрепелнный за магазином
    order_accepting: показатель может ли магазин принемать заказы
    """

    name = models.CharField(_('shop\'s name'), max_length=58)
    url = models.URLField('URL', null=True, blank=True)
    user = models.OneToOneField(CustomUser, verbose_name=_('User'),
                                related_name='shop', blank=True,
                                null=True, on_delete=models.CASCADE)
    order_accepting = models.BooleanField(
        _('order receving status'),
        default=True,
        help_text=_('indicates the shop\'s ability to accept orders')
    )


class ShopDelivery(models.Model):
    shop = models. ForeignKey(Shop,
                              verbose_name=_('shop'),
                              related_name='shop_deliverys',
                              blank=True,
                              on_delete=models.CASCADE)
    delivered_price = models.PositiveIntegerField(_('Delivery price'))
    quantity = models.PositiveIntegerField(_('Quantity'),
                                           help_text=_('Min quantity for price delivery'))

    class Meta:
        verbose_name = _('shop delivered')
        verbose_name_plural = _('list of shop delivery')
        constraints = [
            models.UniqueConstraint(fields=['shop', 'quantity'],
                                    name='unique_shop_delivery'),
        ]
