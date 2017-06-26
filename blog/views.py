from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from blog.models import *
from django.db.models import Q
from blog.forms import RegisterForm, CommentAddForm, ArticleRateForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterUserView(CreateView):
    form_class = RegisterForm
    success_url = "/accounts/login"
    template_name = "registration/register.html"


class IndexListView(ListView):
    queryset = Article.objects.filter(status=1).order_by("-published")
    context_object_name = "article_list"
    template_name = 'index.html'
    paginate_by = 10

    def get_queryset(self):
        context = super(IndexListView, self).get_queryset()
        query = self.request.GET.get("q")
        if query:
            return context.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )
        else:
            return context


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentAddForm(initial={'article': self.object.pk})
        context['rate_form'] = ArticleRateForm(initial={'article': self.object.pk})
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentAddForm
    template_name = "blog/forms/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        qs = Comment.objects.get(id=form.instance.id)
        return JsonResponse({
            'status': 'success',
            'message': 'Комментарий успешно добавлен!',
            'author': qs.author.username,
            'created': qs.created_date.date(),
            'text': qs.comment_text
        })


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['article_list'] = Article.objects.filter(category=self.object, status=1).order_by("-published")
        return context


class UserArticlesView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "blog/user_article_detail.html"
    slug_field = 'id'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "blog/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.filter(user=self.object)
        return context


class ArticleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Article
    template_name = "blog/forms/article_form.html"
    fields = ['title', 'image', 'content', 'category']
    success_url = '/blog'
    success_message = "Статья успешно добавлена! После проверки админом, ваша статья опубликуется."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)


class ArticleRateView(LoginRequiredMixin, CreateView):
    template_name = "blog/forms/article_rate_form.html"
    form_class = ArticleRateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        check = ArticleRating.objects.filter(article=form.instance.article, user=form.instance.user).exists()
        if check:
            return JsonResponse({'status': 'warning', 'message': 'Вы уже голосовали'})
        else:
            form.save()
            qs = ArticleRating.objects.filter(article=form.instance.article)
            return JsonResponse({
                'status': 'success',
                'counts': qs.count()
            })