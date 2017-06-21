from django.contrib import admin
from .models import *


class CategoryModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Category


class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published", "status", "category"]
    list_filter = ["published"]
    search_fields = ["title", "content"]

    class Meta:
        model = Article


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["comment_text", "author", "published", "article"]

    class Meta:
        model = Comment

admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Article, ArticleModelAdmin)
admin.site.register(Comment, CommentModelAdmin)