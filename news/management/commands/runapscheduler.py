import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from news.models import Post, Category
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...
    """
    Если пользователь подписан на какую-либо категорию,
    то каждую неделю ему приходит на почту список новых статей,
    появившийся за неделю с гиперссылкой на них, чтобы пользователь мог перейти и прочесть любую из статей.
    """


    # 1. Взять всех пользователей, у кого есть подписки

    for user in User.objects.all():
        new_posts = {}
        for category in Category.objects.all():
            if user not in category.subscribers.all():
                continue

            # 2. Взять новые статьи данной категории за неделю
            new_posts_items = Post.objects.filter(category__exact=category, create_datetime__gte=datetime.now() - timedelta(days=7))
            new_posts[category] = []
            for new_post in new_posts_items:
                new_posts[category].append({'url': f'http://{Site.objects.get_current().domain}:8000{new_post.get_absolute_url()}',
                                            'preview': new_post.preview()})


        # 3. Сгенерировать html, отправить письмо пользователю
        html_content = render_to_string('news/new_posts_appointment.html', {
            'username': user,
            'posts': new_posts,
        })

        msg = EmailMultiAlternatives(subject='Новые посты за неделю',
                                     body=f'Привет! Новые статьи по категориям:',
                                     from_email=settings.DEFAULT_FROM_EMAIL,
                                     to=[user.email])

        msg.attach_alternative(html_content, 'text/html')

        msg.send()





# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day="*/7"),
            # То же самое что и интервал, но задача триггера таким образом более понятна django
            id="my_job",  # уникальный id
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")