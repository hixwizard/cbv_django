from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404

from .models import Comment


class AuthorshipCheckMixin(UserPassesTestMixin):
    """Миксин для проверки авторства объекта."""

    def test_func(self):
        """Проверяет, является ли пользователь автором объекта."""
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        """Обработка случая, когда у пользователя нет прав."""
        if not self.request.user.is_authenticated:
            return redirect('login')
        return redirect(
            'blog:post_detail',
            post_id=self.kwargs['post_id']
        )


class CommentPostCheckMixin:
    """Миксин для проверки соответствия комментария посту."""

    def get_object(self, queryset=None):
        """Получает комментарий с проверкой соответствия посту."""
        comment = get_object_or_404(
            Comment.objects.select_related('post'),
            id=self.kwargs['comment_id'],
            post_id=self.kwargs['post_id']
        )
        return comment


class CommentUrlMixin:
    """Миксин для получения URL страницы поста с комментариями."""

    def get_success_url(self):
        """Возвращает URL страницы поста."""
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )
