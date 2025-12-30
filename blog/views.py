from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from posts.models import Article, Post, Tutorial
from taggit.models import Tag


def index(request):
    last_posts = Post.objects.filter(
        status=Post.Status.PUBLISHED
    ).order_by("-published_at")[:3]

    featured_posts = Post.objects.filter(
        status=Post.Status.PUBLISHED, 
        is_featured=True
    )[:3]

    ctx = {"featured_posts": featured_posts, "last_posts": last_posts}

    return render(request, "blog/index.html", ctx)


def posts(request):
    all_posts = Post.objects.filter(status=Post.Status.PUBLISHED).order_by(
        "-published_at"
    )

    paginator = Paginator(all_posts, 4)

    page_number = request.GET.get("pagina")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/post_list.html",
        {"page_obj": page_obj, "title": "Todos os Posts"},
    )


def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)

    return render(
        request, "blog/post_detail.html", {"post": post},
    )


def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__name=tag.name).order_by("-published_at")

    paginator = Paginator(posts, 4)
    page_number = request.GET.get("pagina")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "blog/post_list.html", {"page_obj": page_obj, "title": tag.name}
    )


def articles(request):
    articles = Article.objects.filter(status=Post.Status.PUBLISHED).order_by(
        "-published_at"
    )

    paginator = Paginator(articles, 4)
    page_number = request.GET.get("pagina")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/post_list.html",
        {"page_obj": page_obj, "title": Article._meta.verbose_name_plural.title()},
    )


def tutorials(request):
    tutorials = Tutorial.objects.filter(status=Post.Status.PUBLISHED).order_by(
        "-published_at"
    )

    paginator = Paginator(tutorials, 4)
    page_number = request.GET.get("pagina")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/post_list.html",
        {"page_obj": page_obj, "title": Tutorial._meta.verbose_name_plural.title()},
    )
