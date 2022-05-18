from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from accounts.models import CustomUser


def new_order_email(user_id, **kwargs):
    """Отправка письма при изменении статуса заказа"""
    user = CustomUser.objects.get(id=user_id)
    msg = EmailMultiAlternatives(f'Update order\'s status',
                                 'new order',
                                 settings.EMAIL_HOST_USER,
                                 [user.email])
    return msg.send()

