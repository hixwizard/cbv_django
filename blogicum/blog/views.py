from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DetailView, UpdateView, ListView, CreateView, DeleteView
)
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .constants import POSTS_TO_DISPLAY
from .models import Category, Post, Comment
from .forms import (
    PostCreateForm, UserEditForm, UserCreationForm,
    CommentForm)
from .utils import get_posts_queryset
from .mixins import (
    AuthorshipCheckMixin, CommentUrlMixin, CommentPostCheckMixin
)


User = get_user_model()


class IndexView(ListView):
    """Отображает главную страницу со списком опубликованных постов."""

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = POSTS_TO_DISPLAY

    def get_queryset(self):
        """Возвращает QuerySet с опубликованными постами."""
        return get_posts_queryset(filter_flag=True, annotate_flag=True)


class CategoryDetailView(ListView):
    """Отображение списка постов в определённой категории."""

    template_name = "blog/category.html"
    context_object_name = "post_list"
    paginate_by = POSTS_TO_DISPLAY

    def get_category(self):
        """Получает объект категории или вызывает 404."""
        return get_object_or_404(
            Category,
            slug=self.kwargs["slug"],
            is_published=True
        )

    def get_queryset(self):
        """Формирование списка постов для категории."""
        category = self.get_category()
        return get_posts_queryset(
            manager=category.posts,
            filter_flag=True,
            annotate_flag=True
        )

    def get_context_data(self, **kwargs):
        """Добавление категории в контекст."""
        context = super().get_context_data(**kwargs)
        context["category"] = self.get_category()
        return context


class PostDetailView(DetailView):
    """Отображение отдельного поста и его комментариев."""

    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        """Возвращает пост с проверкой прав доступа."""
        post = get_object_or_404(
            get_posts_queryset(),
            pk=self.kwargs['post_id']
        )
        if self.request.user != post.author:
            post = get_object_or_404(
                get_posts_queryset(filter_flag=True),
                pk=self.kwargs['post_id']
            )
        return post

    def get_context_data(self, **kwargs):
        """Добавляет форму комментария и список комментариев в контекст."""
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    """Создание нового поста."""

    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        """Устанавливает текущего пользователя как автора поста."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Возвращает URL профиля пользователя после создания поста."""
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class EditPostView(LoginRequiredMixin, AuthorshipCheckMixin, UpdateView):
    """Редактирование существующего поста."""

    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        """Возвращает URL отредактированного поста."""
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.id}
        )


class DeletePostView(LoginRequiredMixin, AuthorshipCheckMixin, DeleteView):
    """Удаление поста."""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        """Добавляет форму с данными удаляемого поста в контекст."""
        context = super().get_context_data(**kwargs)
        context['form'] = PostCreateForm(instance=self.object)
        return context


class CreateCommentView(LoginRequiredMixin, CreateView):
    """Создание нового комментария к посту."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        """Устанавливает автора комментария и связывает с постом."""
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        """Возвращает URL созданного комментария."""
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class BaseCommentView:
    """Базовый класс для работы с комментариями."""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class EditCommentView(
    LoginRequiredMixin, AuthorshipCheckMixin,
    CommentUrlMixin, CommentPostCheckMixin,
    BaseCommentView, UpdateView
):
    """Редактирование существующего комментария."""

    form_class = CommentForm


class DeleteCommentView(
    LoginRequiredMixin, AuthorshipCheckMixin,
    CommentUrlMixin, CommentPostCheckMixin,
    BaseCommentView, DeleteView
):
    """Удаление комментария."""


class RegistrationView(CreateView):
    """Регистрация нового пользователя."""

    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:index')


class UserProfileView(ListView):
    """Отображает профиль пользователя и его посты."""

    template_name = 'blog/profile.html'
    paginate_by = POSTS_TO_DISPLAY
    context_object_name = 'posts'

    def get_user_profile(self):
        """Получает профиль пользователя или вызывает 404."""
        return get_object_or_404(
            User, username=self.kwargs['username']
        )

    def get_queryset(self):
        """
        Возвращает QuerySet с постами пользователя.
        Для автора показывает все посты, для остальных только опубликованные.
        """
        profile = self.get_user_profile()
        return get_posts_queryset(
            manager=profile.posts,
            filter_flag=self.request.user != profile,
            annotate_flag=True
        )

    def get_context_data(self, **kwargs):
        """Добавляет профиль пользователя в контекст."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_user_profile()
        return context


class EditUserProfileView(LoginRequiredMixin, UpdateView):
    """Позволяет пользователю редактировать свой профиль."""

    model = User
    form_class = UserEditForm
    template_name = 'blog/user.html'

    def get_object(self):
        """Возвращает текущего пользователя."""
        return self.request.user

    def get_success_url(self):
        """Возвращает URL профиля пользователя после успешного обновления."""
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
