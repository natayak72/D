from django.views.generic import DeleteView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post
from .forms import PostCreateForm
from .filters import NewsFilter
# Create your views here.


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

        # TODO context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())

        return context


class NewsCreate(PermissionRequiredMixin, ListView):
    permission_required = ('news.add_post', 'news.change_post')
    model = Post
    template_name = 'news/create.html'
    form_class = PostCreateForm

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