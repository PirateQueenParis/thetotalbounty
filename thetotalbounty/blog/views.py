# Create your views here.
from django.shortcuts import render
from django.db.models import F

from blog.models import Post, Comment


def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
    }
    if not request.user.is_superuser:
        post.view_count = F('view_count') + 1
        post.save()
        post.refresh_from_db()
    return render(request, "blog/detail.html", context)
