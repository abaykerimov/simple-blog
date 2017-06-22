from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category_name = models.CharField(verbose_name=u'Категория', max_length=255)

    class Meta:
        ordering = ('category_name',)
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'

    def __str__(self):
        return self.category_name


class Article(models.Model):
    STATUSES = (
        (1, u'Опубликованные'),
        (0, u'Не опубликованные')
    )
    title = models.CharField(verbose_name=u'Заголовок', max_length=255)
    image = models.ImageField(blank=True, null=True)
    content = models.TextField(verbose_name=u'Текст статьи')
    author = models.ForeignKey(User)
    published = models.DateTimeField(verbose_name=u'Дата добавления', auto_now_add=True)
    status = models.IntegerField(verbose_name=u'Статус статьи', choices=STATUSES)
    category = models.ForeignKey(Category)

    class Meta:
        ordering = ('title',)
        verbose_name = u'Статья'
        verbose_name_plural = u'Статьи'

    def __str__(self):
        return self.title


class ArticleRating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User)
    rate_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('rate_date',)
        verbose_name = u'Рейтинг'
        verbose_name_plural = u'Рейтинги'


class Comment(models.Model):
    comment_text = models.TextField(verbose_name=u'Комментарий')
    author = models.ForeignKey(User)
    published = models.DateTimeField()
    created_date = models.DateTimeField(auto_created=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_date',)
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'

    def __str__(self):
        return self.comment_text


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="")
    date_of_birth = models.DateField(auto_now_add=False, auto_created=False)

    class Meta:
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'