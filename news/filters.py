from django_filters import FilterSet
from .models import Post


class NewsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'create_datetime': ['gt'],
            'header': ['icontains'],
            'author': ['exact']
        }


class CategoryFilter(FilterSet):
    class Meta:
        model = Post
        fields = ['category']
