from django.contrib import admin

# Register your models here.
from .models import *


# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
