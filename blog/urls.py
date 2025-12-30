from django.urls import path
from blog.views import index, posts, post_detail, articles, tutorials, posts_by_tag
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('', index, name="home"),
    path(_('artigos/'), articles, name='articles'),
    path(_('tutoriais/'), tutorials, name='tutorials'),
    path(_('todos-os-posts/'), posts, name="all-posts"),
    path('<slug:post_slug>/', post_detail, name='post-detail'),
    path(_('marcadores/<slug:tag_slug>/'), posts_by_tag, name='posts-by-tag'),
]
