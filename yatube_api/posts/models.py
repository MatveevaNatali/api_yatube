from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

LIMIT = 30


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Указатель группы',
    )
    description = models.TextField(
        verbose_name='Описание группы',
    )

    def __str__(self):
        return self.title[:LIMIT]


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст статьи',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор статьи',
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа статей',
    )

    def __str__(self):
        return self.text[:LIMIT]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Имя автора',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Название поста',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    created = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self) -> str:
        return f'{self.author} прокомментировал: {self.text}'
