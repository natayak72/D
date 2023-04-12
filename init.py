# До включения консоли:
# pip install -r requirements.txt
# python manage.py createsuperuser
import time

# Что вы должны сделать в консоли Django?

# Создать двух пользователей (с помощью метода User.objects.create_user).
print('Creating users...')
from django.contrib.auth.models import User

u1 = User.objects.create_user(username='user1')
u2 = User.objects.create_user(username='user2')

# Создать два объекта модели Author, связанные с пользователями.
print('Creating authors...')
from news.models import *

a1 = Author.objects.create(authorUser=u1)
a2 = Author.objects.create(authorUser=u2)

# Добавить 4 категории в модель Category.
print('Creating categories...')
c1 = Category.objects.create(name='Category 1')
c2 = Category.objects.create(name='Category 2')
c3 = Category.objects.create(name='Category 3')
c4 = Category.objects.create(name='Category 4')

# Добавить 2 статьи и 1 новость.
print('Creating posts...')

ARTICLE_TEXT = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
POSTS_COUNT = 12

article1 = Post.objects.create(author=a1, header='Article header 1', text=ARTICLE_TEXT, type='article')
print('created post 1 of 12')

time.sleep(30)
article2 = Post.objects.create(author=a2, header='Article header 2', text=ARTICLE_TEXT, type='article')
print('created post 2 of 12')

time.sleep(30)
article3 = Post.objects.create(author=a1, header='News header 1', text=ARTICLE_TEXT, type='news')
print('created post 3 of 12')

time.sleep(30)
article4 = Post.objects.create(author=a1, header='News header 2', text=ARTICLE_TEXT, type='news')
print('created post 4 of 12')

time.sleep(30)
article5 = Post.objects.create(author=a2, header='Article header 3', text=ARTICLE_TEXT, type='article')
print('created post 5 of 12')

time.sleep(30)
article6 = Post.objects.create(author=a1, header='News header 3', text=ARTICLE_TEXT, type='news')
print('created post 6 of 12')

time.sleep(30)
article7 = Post.objects.create(author=a2, header='Article header 4', text=ARTICLE_TEXT, type='article')
print('created post 7 of 12')

time.sleep(30)
article8 = Post.objects.create(author=a1, header='News header 4', text=ARTICLE_TEXT, type='news')
print('created post 8 of 12')

time.sleep(30)
article9 = Post.objects.create(author=a2, header='Article header 5', text=ARTICLE_TEXT, type='article')
print('created post 9 of 12')

time.sleep(30)
article10 = Post.objects.create(author=a1, header='News header 5', text=ARTICLE_TEXT, type='news')
print('created post 10 of 12')

time.sleep(30)
article11 = Post.objects.create(author=a2, header='Article header 6', text=ARTICLE_TEXT, type='article')
print('created post 11 of 12')

time.sleep(30)
article12 = Post.objects.create(author=a2, header='Article header 7', text=ARTICLE_TEXT, type='article')
print('created post 12 of 12')

# Присвоить им категории
# (как минимум в одной статье/новости должно быть не меньше 2 категорий).
print('Setting categories to posts...')
article1.category.add(c1.id, c2.id)
article2.category.add(c3.id, c4.id)
article3.category.add(c2.id, c3.id)

# Создать как минимум 4 комментария к разным объектам модели Post
# (в каждом объекте должен быть как минимум один комментарий).
print('Creating comments...')
comm1 = Comment.objects.create(post=article1, author=a1.authorUser, text='Good post!')
time.sleep(10)
comm2 = Comment.objects.create(post=article1, author=a2.authorUser, text='Bad post!')
time.sleep(10)
comm3 = Comment.objects.create(post=article2, author=a2.authorUser, text='Another good post!')
time.sleep(10)
comm4 = Comment.objects.create(post=article3, author=a2.authorUser, text='Bad post!')

# Применяя функции like() и dislike() к статьям/новостям и комментариям,
# скорректировать рейтинги этих объектов.
print('Adding likes and dislikes to posts...')
article1.like()
article1.like()
article1.dislike()

comm1.like()
comm1.like()
comm1.dislike()

comm2.like()
comm2.like()
comm2.dislike()

comm3.like()
comm3.like()
comm3.dislike()

comm4.like()
comm4.like()
comm4.dislike()

# Обновить рейтинги пользователей.
print('Updating authors ratings...')
a1.update_rating()
a2.update_rating()

# Вывести username и рейтинг лучшего пользователя
# (применяя сортировку и возвращая поля первого объекта).
print('Get best author...')
bu = Author.objects.all().order_by('-rating').values('authorUser', 'rating')[0]

# Вывести дату добавления, username автора, рейтинг,
# заголовок и превью лучшей статьи,
# основываясь на лайках/дислайках к этой статье.

# лучшая статья
bp = Post.objects.all().order_by('-rating')[0]
print(f'Best post: {bp.preview()}')
print(f'Author: {bp.author.authorUser.username}')
print(f'Add date: {bp.create_datetime}')
print(f'Rating: {bp.rating}')
print(f'Header: {bp.header}')

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
comments = Comment.objects.filter(post=bp)
print('')
print('\nComments for this post:')
for comment in comments:
    print(
        f'User {comment.author.username} says (at {comment.create_datetime}): {comment.text}; comm rating: {comment.rating}\n')
