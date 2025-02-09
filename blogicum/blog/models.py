from django.contrib.auth import get_user_model
from django.db import models

from .constants import MAX_CHARACTERS, LEN_STR


User = get_user_model()


class BasePublishCreatedAtModel(models.Model):
    """Базовая абстракная модель для общих полей."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Category(BasePublishCreatedAtModel):
    """Определяет свойства категорий."""

    title = models.CharField(
        max_length=MAX_CHARACTERS,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.'),
    )

    class Meta:
        """Дополнительные параметры."""

        verbose_name: str = 'категория'
        verbose_name_plural: str = 'Категории'

    def __str__(self) -> str:
        return (
            self.title[:LEN_STR]
            + '...' if len(self.title) > LEN_STR else self.title
        )


class Location(BasePublishCreatedAtModel):
    """Определяет свойства местоположения."""

    name = models.CharField(
        max_length=MAX_CHARACTERS,
        verbose_name='Название места',
    )

    class Meta:
        """Дополнительные параметры."""

        verbose_name: str = 'местоположение'
        verbose_name_plural: str = 'Местоположения'

    def __str__(self) -> str:
        return (
            self.name[:LEN_STR]
            + '...' if len(self.name) > LEN_STR else self.name
        )


class Post(BasePublishCreatedAtModel):
    """Определяет свойства поста."""

    title = models.CharField(
        max_length=MAX_CHARACTERS,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем'
                   ' — можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    image = models.ImageField(
        blank=True,
        verbose_name='Изображение'
    )

    class Meta:
        """Дополнительные параметры."""

        ordering = ['-pub_date']
        verbose_name: str = 'публикация'
        verbose_name_plural: str = 'Публикации'
        default_related_name = 'posts'

    def __str__(self) -> str:
        """Параметр для отображения названия."""
        return (
            self.title[:LEN_STR]
            + '...' if len(self.title) > 10 else self.title
        )


class Comment(BasePublishCreatedAtModel):
    """Определяет свойства комментария."""

    text = models.TextField(verbose_name='Текст комментария',)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('created_at',)

    def __str__(self) -> str:
        """Параметр для отображения названия."""
        return (
            self.text[:LEN_STR]
            + '...' if len(self.text) > 10 else self.text
        )
