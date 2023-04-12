from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BaseRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    # в классе мета, описана модель, по которой будет строиться форма и нужные поля
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class BasicSignupForm(SignupForm):
    def save(self, request):
        # вызываем этот же метод класса-родителя, чтобы необходимые проверки и сохранение в модель User были выполнены
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)  # user_set, возвращающий список всех пользователей этой группы

        # Обязательным требованием метода save() является возвращение объекта модели User по итогу выполнения функции.
        return user
