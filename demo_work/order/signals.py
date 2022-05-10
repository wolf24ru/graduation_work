from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver, Signal

from accounts.models import CustomUser

new_order = Signal()

@receiver(new_order)
def new_order_singal(user_id, **kwargs):
    """Отправка письма при изменении статуса заказа"""
    user = CustomUser.objects.get(id=user_id)
    msg = EmailMultiAlternatives(f'Update order\'s status',
                                 'new order',
                                 settings.EMAIL_HOST_USER,
                                 [user.email])
    msg.send()
