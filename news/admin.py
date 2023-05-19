from django.contrib import admin

# Register your models here.
from .models import *


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('author', 'header', 'rating', 'create_datetime', 'type')
    list_filter = ['category', 'author']
    search_fields = ['header']


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'rating')
    list_filter = ('authorUser',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'create_datetime', 'rating', )
    list_filter = ('author', )



admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
