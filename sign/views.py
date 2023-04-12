# Create your views here.

from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User
from .forms import BaseRegistrationForm

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class LoginView(TemplateView):
    template_name = 'sign/login.html'


class BaseRegisterView(CreateView):
    # модель формы, которую реализует данный дженерик;
    model = User
    form_class = BaseRegistrationForm
    success_url = '/news'


@login_required
def make_me_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)

    return redirect('/news/')
