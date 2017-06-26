from blog.models import Category, Comment


def category(request):
    return {"category_list": Category.objects.all()}


def comments(request):
    return {"comments_list": Comment.objects.order_by("-created_date")[:10]}