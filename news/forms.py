from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from .models import Post

class PostCreateForm(ModelForm):
    # дополнительное поле в форме
    # в классе мета, описана модель, по которой будет строиться форма и нужные поля
    class Meta:
        model = Post
        fields = ['author', 'category', 'header', 'text', 'type']
