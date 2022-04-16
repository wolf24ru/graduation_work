from django.contrib.auth.models import AbstractUser
from django.db import models


# class Permissions(models.Model):
#     '''
#     Класс для получения разрешений.
#
#     status: название статуса
#     input_admin: наличие доступа в админку
#     update: возможность изменять позиции
#     payment: возможность оплачивать покупки
#     write_comment: возможность писать коментарии(открывается только
#     после выполнения заказа)
#     delete: возможность удалять позиции
#     bun: забаненный пользователь
#     '''
#     status = models.CharField(max_length=30)
#     input_admin = models.BooleanField()
#     update = models.BooleanField()
#     payment = models.BooleanField()
#     write_comment = models.BooleanField()
#     delete = models.BooleanField()
#     bun = models.BooleanField()
#
# # class Basket(models.Model):
# #     ...


class CustomUser(AbstractUser):
    '''
    Класс пользователя.

    nikname: никнайм пользователя

    email: email
    password: пороль
    phone_number: номер телефона
    permissions: разрешения из таблицы Permissions

    Возможно в них нет необходимости, а получать доступ у ним через смежные
    таблицы
    order: список заказов из тиблицы Order

    реализовать чуть позже
    bonus: список бонусов пользователя и тиблице Bonus
    basket: корзина пользователя, должна хранить добавленные в нее позиции и
    очещаться после покупки
    '''

    username = models.CharField('Никнейм', max_length=58, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField('Пароль', max_length=200)
    phone_number = models.CharField('Номер телефона', max_length=12, unique=True)
    # id_permission = models.ForeignKey(Permissions,
    #                                    verbose_name='Разрешение',
    #                                    related_name='permission',
    #                                   related_query_name='custom_user',
    #                                   on_delete=models.DO_NOTHING,
    #                                   blank=True,
    #                                   null=True
    #                                   )
    # bonus = ...
    # order = ...

    # basket = ...


class UserInfo(models.Model):
    '''
        Класс описывающий пользователя.

        name: имя пользователя
        surname: фамилия пользователя
        country: страна проживания
        region: регион проживания
        city: город проживания
    '''
    id_custom_user = models.OneToOneField(CustomUser,
                                          on_delete=models.CASCADE,
                                          primary_key=True,
                                          unique=True,
                                          related_name='user',
                                          related_query_name='user_info'
                                          )
    name = models.CharField('Имя', max_length=58, blank=True)
    surname = models.CharField('Фамилия', max_length=80, blank=True)
    country = models.CharField('Страна', max_length=58, blank=True)
    region = models.CharField('Регион', max_length=58, blank=True)
    city = models.CharField('Город', max_length=58, blank=True)
