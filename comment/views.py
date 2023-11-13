from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CommentForm
from .models import *
from Post.models import Post


@login_required
def comment_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            username = post.user.username
            return redirect('post_detail', username=username, post_id=post_id)
    else:
        comment_form = CommentForm()

    return render(request, 'posts/posts_detail.html',
                  {'post': post, 'comments': comments, 'comment_form': comment_form})


@login_required
def delete_comment(request, username, post_id, comment_id):
    try:
        post = Post.objects.get(id=post_id)
        comment = get_object_or_404(Comment, id=comment_id, post=post)

        if request.user == comment.user or request.user.is_superuser:
            # Only allow deletion if the logged-in user is the owner of the comment
            comment.delete()
            return redirect('post_detail', username=username, post_id=post_id)
        else:
            # If the logged-in user is not the owner, return a forbidden response
            return HttpResponseForbidden("You are not allowed to delete this comment.")
    except Post.DoesNotExist:
        pass
    return redirect('post_detail', username=username, post_id=post_id)