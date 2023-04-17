import datetime

from django.views.generic import DeleteView, ListView, DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category, User
from .forms import PostCreateForm
from .filters import NewsFilter, CategoryFilter

# Create your views here.

FROM_EMAIL = 'yacyna.pavel@yandex.ru'


class NewsDonos(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/donos.html')

    def post(self, request, *args, **kwargs):
        donos_date = datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d')
        donos_client_name = request.POST['client_name']
        donos_message = request.POST['message']

        send_mail(subject=f'Уважаемый {donos_client_name}! Ваш донос от {donos_date}:',
                  message=donos_message,
                  from_email=FROM_EMAIL,
                  recipient_list=['yacyna.pavel1@gmail.com'])

        return redirect('news_donos')


class CategorySubscribe(DetailView):
    model = Category
    template_name = 'news/subscribe_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        x = 1
        context['subscribers'] = self.object.subscribers.all()
        return context

    def post(self, request, *args, **kwargs):
        x = 1
        user = User.objects.get(pk=request.user.pk)
        category = Category.objects.get(pk=kwargs.get("pk"))
        print(f'Пользователем {user} осуществлена подписка на категорию {category}!')

        category.subscribers.add(user)
        return redirect('news_list')


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

        context = super().get_context_data(**kwargs)

        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()

        filter = CategoryFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = filter

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
    def post(self, request):
        author_id = request.POST.get('author')
        categories = request.POST.getlist('category')
        header = request.POST.get('header')
        text = request.POST.get('text')
        post_type = request.POST.get('type')
        new_post = Post(author_id=author_id, header=header, text=text, type=post_type)
        new_post.save()

        for category_id in categories:
            new_post.category.add(category_id)

            subscribers = Category.objects.get(pk=category_id).subscribers.all()

            recipients_list = []
            for subscriber in subscribers:
                recipients_list.append(subscriber.email)

            send_mail(subject=f'Вышла новая статья из категории {category_id}!',
                      message=new_post.preview(),
                      from_email=FROM_EMAIL,
                      recipient_list=recipients_list)

        new_post.save()

        return redirect('news_list')

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
