# forms.py
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'picture', 'video', 'post_type']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Make the 'post_type' field not required
        self.fields['post_type'].required = False

    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        if picture and picture.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError("The maximum file size that can be uploaded is 25MB")
        return picture

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video and video.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError("The maximum file size that can be uploaded is 25MB")
        return video

    def clean(self):
        cleaned_data = super().clean()
        post_type = cleaned_data.get('post_type')
        content = cleaned_data.get('content')
        content = cleaned_data.get('content')
        picture = cleaned_data.get('picture')
        video = cleaned_data.get('video')

        if not content and not picture and not video:
            raise ValidationError("You must provide either content, a picture, or a video.")

        # If the post_type is 'picture' or 'video', the content field is not required.
        if post_type in ['picture', 'video']:
            if not content:
                cleaned_data['content'] = ''  # Set content to an empty string if not provided
        return cleaned_data