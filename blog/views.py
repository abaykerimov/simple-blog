from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from blog.models import *
from blog.forms import RegisterForm, CommentAddForm
from django.contrib.messages.views import SuccessMessageMixin


class RegisterUserView(CreateView):
    form_class = RegisterForm
    success_url = "/accounts/login"
    template_name = "registration/register.html"


class IndexListView(ListView):
    queryset = Article.objects.filter(status=1).order_by("-published")
    context_object_name = "article_list"
    template_name = 'index.html'
    paginate_by = 10


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentAddForm(initial={'article': self.object.pk})
        return context


class CommentCreate(CreateView):
    model = Article
    form_class = CommentAddForm
    template_name = "blog/forms/comment_form.html"
    success_message = "Комментарий успешно добавлен!"
    #success_url = '/blog'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CommentCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CommentCreate, self).form_valid(form)




class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['article_list'] = Article.objects.filter(category=self.object, status=1).order_by("-published")
        return context


class UserArticlesView(DetailView):
    model = User
    template_name = "blog/user_article_detail.html"
    slug_field = 'id'


class UserDetailView(DetailView):
    model = User
    template_name = "blog/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.filter(user=self.object)
        return context


class ArticleCreate(SuccessMessageMixin, CreateView):
    model = Article
    template_name = "blog/forms/article_form.html"
    fields = ['title', 'image', 'content', 'category']
    success_url = '/blog'
    success_message = "Статья успешно добавлена! После проверки админом, ваша статья опубликуется."

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ArticleCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleCreate, self).form_valid(form)


