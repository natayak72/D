import datetime

from django.views.generic import DeleteView, ListView, DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from .models import Post, Category
from .forms import PostCreateForm
from .filters import NewsFilter, CategoryFilter
# Create your views here.


class NewsDonos(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/donos.html')

    def post(self, request, *args, **kwargs):
        donos_date = datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d')
        donos_client_name = request.POST['client_name']
        donos_message = request.POST['message']

        send_mail(subject=f'Уважаемый {donos_client_name}! Ваш донос от {donos_date}:',
                  message=donos_message,
                  from_email='yacyna.pavel@yandex.ru',
                  recipient_list=['yacyna.pavel1@gmail.com'])

        return redirect('news_donos')


class NewsSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsDelete(LoginRequiredMixin, DeleteView):
    queryset = Post.objects.all()
    template_name = 'news/delete.html'
    success_url = '/news/'


class NewsInstance(DetailView):
    model = Post
    template_name = 'news/item.html'
    context_object_name = 'news'
    queryset = Post.objects.all()


class NewsList(ListView):
    model = Post
    template_name = 'news/list.html'
    context_object_name = 'news_list'
    allow_empty = True  # Возвращает пустой список, если объектов нет (если False - будет 404)
    ordering = ['-create_datetime']
    paginate_by = 5

    def get_context_data(self, **kwargs):

        print(f'get_context_data:')
        context = super().get_context_data(**kwargs)

        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()

        filter = CategoryFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = filter
        data = filter.data
        x = 1
        try:
            filter_data = filter.data.getlist('category')
        except AttributeError:
            print('не выбраны категории!')
            filter_data = []
            pass

        x = 1
        try:
            categories = [Category.objects.get(id=int(category_id)) for category_id in filter.data.getlist('category')]
        except AttributeError:
            categories = []
        context['choosed'] = categories
        x = 1
        return context

    # def get(self, request, *args, **kwargs):
    #     print('news get')
    #     return redirect('news_list')


class NewsCreate(PermissionRequiredMixin, ListView):
    permission_required = ('news.add_post', 'news.change_post')
    model = Post
    template_name = 'news/create.html'
    form_class = PostCreateForm

    # TODO после реализации подписки на категорию
    # def post(self, request):
    #     print('post!')
        # 1. взять данные из поста
        # 2. создать пост
        # 3. взять всех подписчиков из каждой категории поста
        # 4. отправить каждому сообщение на эл. почту
        # return redirect('news_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostCreateForm
        return context


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post', 'news.change_post')
    model = Post
    template_name = 'news/create.html'
    form_class = PostCreateForm

    def get_object(self, queryset=None):
        return Post.objects.get(id=self.kwargs.get('pk'))