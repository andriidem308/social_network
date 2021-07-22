"""Social Network Views."""
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View

from .forms import PostForm
from .models import Like, Post, UserProfile


class PostListView(View):
    """Posts in ListView class."""

    def get(self, request, *args, **kwargs):
        """Show posts in ListView for GET method."""
        posts = Post.objects.all()
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'social/index.html', context)

    def post(self, request, *args, **kwargs):
        """Show posts in ListView for POST method."""
        posts = Post.objects.all()
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'social/index.html', context)


class AddLike(LoginRequiredMixin, View):
    """AddLike class."""

    def post(self, request, pk, *args, **kwargs):
        """Add or Remove a like from post."""
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)
            Like.objects.create(from_user=request.user, to_user=post.author, post=post)

        if is_like:
            post.likes.remove(request.user)

        response = request.POST.get('next', '/')
        return HttpResponseRedirect(response)


def likes_analytics(request):
    """Calculate how many likes were made from date to date."""
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if date_from is None:
        date_from = Like.objects.order_by('date')[0].date

    if date_to is None:
        date_to = datetime.datetime.now()

    response = {
        'date_from': date_from,
        'date_to': date_to,
        'likes_amount': Like.objects.filter(date__range=[date_from, date_to]).count()
    }

    return JsonResponse(response)


def last_activity(request, username):
    """Show when the specific user log in and was active last time."""
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user__username=username)
    last_login_time = user.last_login
    last_visit_time = user_profile.last_visit

    response = {
        'user': username,
        'last_login': last_login_time,
        'last_visit': last_visit_time
    }

    return JsonResponse(response)
