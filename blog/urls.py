from django.conf.urls import url, include
from blog.views import *

urlpatterns = [
    url(r'^$', IndexListView.as_view()),
    url(r'^article/(?P<pk>[-\w]+)/$', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^(?P<pk>[-\w]+)/$', CategoryDetailView.as_view(), name="category"),
    url(r'^(?P<pk>[-\w]+)/articles/$', UserArticlesView.as_view(), name="user_article"),
    url(r'^user/(?P<pk>[-\w]+)/$', UserDetailView.as_view(), name="user_profile"),
    url(r'^post/create/$', ArticleCreate.as_view(), name="article_create"),
    url(r'^comment/create/$', CommentCreate.as_view(), name="comment_create"),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # url(r'^$', "blog.views.article_list"),
    # url(r'^create/$', "blog.views.article_create"),
    # url(r'^detail/$', "blog.views.article_detail"),
    # url(r'^edit/$', "blog.views.article_edit"),
    # url(r'^delete/$', "blog.views.article_delete"),
]