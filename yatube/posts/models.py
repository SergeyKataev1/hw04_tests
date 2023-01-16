from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    class Meta:
        verbose_name_plural = 'Группы'

    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальная страница группы'
    )
    description = models.TextField(verbose_name='Описание')

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    class Meta:
        ordering = ('-pub_date', )
        verbose_name_plural = 'Посты'

    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа'
    )

    def __str__(self) -> str:
        return self.text
