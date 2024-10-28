# Create your views here.
from django.core.mail import mail_admins
from django.shortcuts import render
from django.db.models import F
from django.http import HttpResponseRedirect

from blog.models import Post, Comment, UserProfile
from blog.forms import CommentForm, DisplayNameForm
from thetotalbounty.utils import get_user_display_name


def blog_index(request):
    posts = Post.objects.published().all().order_by("-created_on")
    profile = None
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user)
    context = {
        "posts": posts,
        "profile": profile,
    }
    return render(request, "blog/index.html", context)


def blog_category(request, category):
    posts = Post.objects.published().filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)


def blog_detail(request, slug):
    post = Post.objects.published().get(slug=slug)
    comment_form = CommentForm()
    display_name = ''
    if request.user.is_authenticated:    
        display_name = get_user_display_name(request.user, UserProfile.objects)
    display_name_form = DisplayNameForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            comment = Comment(author=request.user, body=body, post=post)
            comment.save()
            mail_admins("User " + str(request.user.userprofile) + " has left a comment on " + post.title, "User " + str(request.user.userprofile) + " has left a comment on " + post.title + ": " + body)
            return HttpResponseRedirect(request.path_info)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "display_name": display_name,
        "comment_form": comment_form,
        "display_name_form": display_name_form
    }
    if not request.user.is_superuser:
        post.view_count = F('view_count') + 1
        post.save()
        post.refresh_from_db()
    return render(request, "blog/detail.html", context)

def display_name_change(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = DisplayNameForm(request.POST)
            if form.is_valid():
                profiles = UserProfile.objects.filter(user=request.user)
                if profiles.count() > 0:
                    profile = profiles[0]
                    profile.display_name = form.cleaned_data['name']
                else:
                    profile = UserProfile(display_name=form.cleaned_data['name'], user=request.user)
                profile.save()
    return HttpResponseRedirect(request.POST.get('next', '/')) 
