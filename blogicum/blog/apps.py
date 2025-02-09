from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Название приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name: str = 'Блог'
