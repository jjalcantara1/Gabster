import os
import random

from django.db import models
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from accounts.models import UserAccount
from django.dispatch import receiver


# Create your models here.
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_picture_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'pictures/{final_filename}'.format(new_filename=new_filename, final_filename=final_filename)


def upload_video_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'videos/{final_filename}'.format(new_filename=new_filename, final_filename=final_filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, blank=True, null=True)
    post_type = models.CharField(max_length=20, choices=[('picture', 'Picture'), ('video', 'Video')], default=None,
                                 null=True)
    picture = models.ImageField(upload_to=upload_picture_path, blank=True, null=True, default=None)
    video = models.FileField(upload_to=upload_video_path, blank=True, null=True, default=None)
    updated = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(UserAccount, related_name='liked_posts', blank=True)

    def __str__(self):
        if self.post_type == 'picture':
            return os.path.basename(self.picture.name)
        if self.post_type == 'video':
            return os.path.basename(self.video.name)
        else:
            return str(self.content)

    def __repr__(self):
        return f"Post('{self.content}', '{self.createdAt}')"

    def create_post(self, content, user, post_type=None, picture=None, video=None):
        post = Post()
        post.content = content
        post.user = user
        post.post_type = post_type
        post.picture = picture
        post.video = video
        post.save()
        return post

    def comment_count(self):
        return self.comment_set.count()

@receiver(post_save, sender=Post)
def create_post(sender, instance, created, **kwargs):
    if created:
        UserLike.objects.create(voter=instance.user, post=instance)


class UserLike(models.Model):
    voter = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('voter', 'post')

    def __str__(self):
        return str(self.voter)
