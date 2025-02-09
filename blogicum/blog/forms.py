from django.forms import ModelForm, DateTimeInput
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm
)

from .models import Post, Comment

User = get_user_model()


class UserCreationForm(DjangoUserCreationForm):
    """Форма регистрации нового пользователя."""

    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserEditForm(ModelForm):
    """Форма для редактирования пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class PostCreateForm(ModelForm):
    """Форма создания нового поста."""

    class Meta:
        model = Post
        fields = (
            'title', 'text', 'pub_date', 'location',
            'category', 'image', 'is_published'
        )
        widgets = {
            'pub_date': DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={'type': 'datetime-local'}),
        }


class CommentForm(ModelForm):
    """Форма комментария."""

    class Meta:
        model = Comment
        fields = ('text',)
