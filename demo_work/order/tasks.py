from celery import shared_task
from celery.utils.log import get_task_logger

from order.emails import new_order_email

loger = get_task_logger(__name__)


@shared_task
def new_order_email_task(user_id):
    loger.info('send email')
    return new_order_email(user_id=user_id)
