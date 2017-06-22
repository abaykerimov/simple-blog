from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic import *
from blog.models import *


class IndexListView(ListView):
    queryset = Article.objects.filter(status=1).order_by("-published")
    context_object_name = "article_list"
    template_name = 'index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.select_related()
        return context


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['article_list'] = Article.objects.select_related()
        return context


class UserArticlesView(DetailView):
    model = User
    template_name = "blog/user_article_detail.html"
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super(UserArticlesView, self).get_context_data(**kwargs)
        context['article_list'] = Article.objects.select_related()
        return context


class UserDetailView(DetailView):
    model = User
    template_name = "blog/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['user_profile'] = User.objects.select_related()
        return context


class CommentCreate(CreateView):
    model = Comment
    fields = ['comment_text']
    template_name = "blog/article_detail.html"
