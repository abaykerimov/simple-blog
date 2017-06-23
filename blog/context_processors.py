from blog.models import Category
from django.views.generic import ListView


def category(request):
    return {"category_list": Category.objects.all()}
