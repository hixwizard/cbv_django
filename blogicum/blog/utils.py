from django.db.models import QuerySet, Count
from django.utils import timezone

from .models import Post


def get_posts_queryset(
        manager=Post.objects,
        filter_flag=False,
        annotate_flag=False
) -> QuerySet:
    """
    Возвращает оптимизированный QuerySet для постов.
    manager: Менеджер модели (по умолчанию Post.objects)
    filter_flag: Флаг для фильтрации неопубликованных постов
    annotate_flag: Флаг для добавления аннотации с количеством комментариев
    """
    queryset = manager.select_related(
        'author',
        'location',
        'category'
    )
    if filter_flag:
        queryset = queryset.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
    if annotate_flag:
        queryset = queryset.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
    return queryset
