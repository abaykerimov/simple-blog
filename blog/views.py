from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView
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
        context['user_articles'] = Article.objects.select_related()
        context['user_comments'] = Comment.objects.select_related()
        return context


class CommentCreate(CreateView):
    model = Comment
    fields = ['comment_text', 'article']
    template_name = "blog/forms/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CommentCreate, self).form_valid(form)


class ArticleCreate(CreateView):
    model = Article
    template_name = "blog/forms/article_form.html"
    fields = ['title', 'image', 'content', 'category']
    success_url = '/blog'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleCreate, self).form_valid(form)


