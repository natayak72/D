from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.DO_NOTHING, default=1)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # 1. получить рейтинги всех статей автора
        posts_likes = 0
        comments_likes = 0
        comments_for_post_likes = 0

        posts = Post.objects.filter(author=self)
        for post in posts:
            posts_likes += post.rating

            # 3. получить рейтинги всех комментариев к статьям автора
            comments_for_post = Comment.objects.filter(post=post)
            for comment in comments_for_post:
                comments_for_post_likes += comment.rating

        # 2. получить рейтинги всех комментариев
        comments = Comment.objects.filter(author__username=self.authorUser.username)
        for post in comments:
            comments_likes += post.rating

        self.rating += posts_likes * 3
        self.rating += comments_likes
        self.rating += comments_for_post_likes

        self.save()

    def __str__(self):
        return self.authorUser.username


class Category(models.Model):
    name = models.CharField(unique=True, default='', max_length=255)

    def __str__(self):
        return self.name


post_types = [('article', 'Статья'),
              ('news', 'Новость')]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category)
    header = models.CharField(max_length=255, default='')
    text = models.TextField(default='')
    rating = models.IntegerField(default=0)
    create_datetime = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=255, choices=post_types)

    """
    from news.models import *
    a = Author.objects.all()[0]
    a.update_rating()
    """

    def __str__(self):
        return f'{self.header} ({self.create_datetime}): {self.preview()}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:50]}...'

    def get_absolute_url(self):
        return f'/news/{self.id}'



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    text = models.TextField(default='')
    create_datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'От автора {self.author} к посту {self.post.header} ({self.post.author}) : {self.text[0:100]}...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

