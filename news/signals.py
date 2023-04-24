from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post, Category
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse

from datetime import datetime, timedelta


@receiver(post_save, sender=Post)
def notify_post_created(instance, **kwargs):
    subject = f'Создана статья: {instance.header}'
    message = instance.preview()

    # 1. Получить все категории
    post_categories = instance.category.all()

    # 2. Получить всех подписчиков всех категорий
    recipients_list = []
    for category in post_categories:
        x = 1
        subscribers = Category.objects.get(pk=category.id).subscribers.all()
        for subscriber in subscribers:
            recipients_list.append(subscriber.email)

    # 3. Отправить письма
    send_mail(subject=subject,
              message=message,
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=recipients_list)


@receiver(pre_save, sender=Post)
def post_number_per_day_control(instance, **kwargs):
    """
    Один пользователь не может публиковать более трёх новостей в сутки
    """
    # 1. Получить пользователя
    author = instance.author

    # 2. Получить число постов этого пользователя с датой создания сегодня
    post_last_day = Post.objects.filter(author=author, create_datetime__gte=datetime.now() - timedelta(hours=24))
    post_last_day_count = len(post_last_day)
    # 3. Если это число более трёх - не дать сохранить
    if post_last_day_count > 3:
        raise Exception('Один пользователь не может публиковать более трёх новостей в сутки')
