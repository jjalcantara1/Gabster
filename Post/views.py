from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from accounts.models import UserAccount
from comment.forms import CommentForm
from comment.models import Comment
from .models import Post, UserLike
from django.urls import reverse_lazy
from django import forms
from Post.forms import PostForm
from django.contrib import messages


@login_required
def create_post(request, username):
    if request.user.username != username:
        raise Http404("You are not allowed to create a post on this profile.")

    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            user = request.user
            print(request.POST)
            post = form.save(commit=False)
            post.user = user
            post.save()

            return redirect('profile', username=username)
    else:
        form = PostForm()

    return render(request, 'posts/post.html', {'form': form})


@login_required
def post_detail(request, username, post_id):
    user = get_object_or_404(UserAccount, username=username)
    post = get_object_or_404(Post, pk=post_id, user=user)
    comments = Comment.objects.filter(post=post)  # Get the comments for the post

    user_like = None
    if request.user.is_authenticated:
        try:
            user_like = UserLike.objects.get(voter=request.user, post=post)
        except UserLike.DoesNotExist:
            user_like = None

    # Instantiate an empty comment form
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('post_detail', username=username, post_id=post_id)

    return render(request, 'Posts/posts_detail.html', {
        'user': user,
        'post': post,
        'user_like': user_like,
        'comments': comments,  # Add the comments to the context
        'comment_form': comment_form,  # Add the comment form to the context
    })





def like(request, username, post_id):
    user = request.user
    target_post = get_object_or_404(Post, pk=post_id)

    user_like, created = UserLike.objects.get_or_create(voter=user, post=target_post)

    if created or not user_like.is_liked:
        user_like.is_liked = True
        target_post.likes += 1
        target_post.liked_by.add(user)
    else:
        user_like.is_liked = False
        target_post.likes -= 1
        target_post.liked_by.remove(user)

    user_like.save()
    target_post.save()
    target_post.refresh_from_db()
    return JsonResponse({'likes': target_post.likes})



@login_required
def get_likes(request, post_id, username):
    post = get_object_or_404(Post, pk=post_id)
    liked_users = [{
        'username': user.username,
        'profile_image': user.profile_image.url if user.profile_image else None
    } for user in post.liked_by.all()]

    return JsonResponse({'liked_users': liked_users})

@login_required
def likedby(request, post_id, username):
    post = Post.objects.get(id=post_id)
    liked_users = [
        {
            'username': user_like.voter.username,
            'profile_image': user_like.voter.profile_image.url if user_like.voter.profile_image else None,
            'fontColor': user_like.voter.fontColor,
            'color': user_like.voter.color,
        }
        for user_like in UserLike.objects.filter(post=post, is_liked=True)
    ]

    return render(request, 'posts/liked_by.html', {'post': post, 'liked_users': liked_users})


@login_required
def delete_post(request, username, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if request.user == post.user or request.user.is_superuser:
            # Only allow deletion if the logged-in user is the owner of the post
            post.delete()
            return redirect('profile', username=username)
        else:
            # If the logged-in user is not the owner, return a forbidden response
            return HttpResponseForbidden("You are not allowed to delete this post.")
    except Post.DoesNotExist:
        pass

    return redirect('profile', username=username)


# @login_required
# def customization(request, username):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = request.user
#
#             post = form.save(commit=False)
#             post.user = user
#             post.save()
#
#             return redirect('profile', username=username)
#     else:
#         form = PostForm()
#
#     return render(request, 'customization/customization.html', {'form': form})
