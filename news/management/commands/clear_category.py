from django.core.management.base import BaseCommand, CommandError
from news.models import Category, PostCategory, Post


class Command(BaseCommand):
    help = 'Данная команда удаляет все новости указанной категории.'
    missing_args_message = 'Не передано название категории!'

    def add_arguments(self, parser):
        parser.add_argument('category', nargs='+', type=str)

    def handle(self, *args, **options):
        category_name_to_delete = options['category']
        for category_name in category_name_to_delete:
            self.stdout.readable()
            self.stdout.write(f'Удалить все новости категории {category_name}? Введите \"yes\", если да.')
            answer = input()

            if answer == 'yes':
                for post in Post.objects.filter(category__name__exact=category_name):
                    post.delete()

        return ''
