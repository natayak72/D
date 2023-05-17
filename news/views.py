import datetime

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.views.generic import DeleteView, ListView, DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Post, Category, User, Author
from .forms import PostCreateForm
from .filters import NewsFilter, CategoryFilter

# Create your views here.


@login_required
def make_me_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)

    Author.objects.create(authorUser_id=user.id)

    return redirect('/news/')


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
        return context


class NewsCreate(PermissionRequiredMixin, ListView):
    permission_required = ('news.add_post', 'news.change_post')
    model = Post
    template_name = 'news/create.html'
    form_class = PostCreateForm

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

            html_content = render_to_string('news/post_appointment.html', {
                'username': request.user,
                'header': new_post.header,
                'preview': new_post.preview(),
                'url': f'http://{Site.objects.get_current().domain}:8000{new_post.get_absolute_url()}'
            })

            msg = EmailMultiAlternatives(subject=new_post.header,
                                         body=f'Здравствуй, {request.user}. Новая статья в твоём любимом разделе!',
                                         from_email=settings.DEFAULT_FROM_EMAIL,
                                         to=recipients_list)

            msg.attach_alternative(html_content, 'text/html')

            msg.send()

            # send_mail(subject=f'Вышла новая статья из категории {category_id}!',
            #           message=new_post.preview(),
            #           from_email=FROM_EMAIL,
            #           recipient_list=recipients_list)

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
