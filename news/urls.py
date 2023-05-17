from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import cache_page


from .views import *

urlpatterns = [
    path('', cache_page(60 * 1)(NewsList.as_view()), name='news_list'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('category_subscribe/<int:pk>', CategorySubscribe.as_view(), name='news_category_subscribe'),
    path('become_author/', make_me_author, name='become_author'),
    path('<int:pk>/edit', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
    path('<int:pk>', cache_page(60 * 5)(NewsInstance.as_view()), name='news_item')
]