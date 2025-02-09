from http import HTTPStatus

from django.views.generic import TemplateView
from django.shortcuts import render


class AboutView(TemplateView):
    """Отображение страницы о нас."""

    template_name = "pages/about.html"


class RulesView(TemplateView):
    """Отображение страницы правил."""

    template_name = "pages/rules.html"


def page_not_found(request, exception):
    """Обработчик ошибки 404."""
    return render(
        request,
        'pages/404.html',
        status=HTTPStatus.NOT_FOUND
    )


def server_error(request):
    """Обработчик ошибки сервера."""
    return render(
        request,
        'pages/500.html',
        status=HTTPStatus.INTERNAL_SERVER_ERROR
    )


def csrf_failure(request, reason="", exception=None):
    """Обработчик ошибки CSRF."""
    return render(
        request,
        'pages/403csrf.html',
        status=HTTPStatus.FORBIDDEN
    )
