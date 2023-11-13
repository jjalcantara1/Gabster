from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from accounts.models import UserAccount

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = [
            'profile_image',
            'profile_cover',
            'profile_song',
            'profile_background',
            'hide_email',
            'bio',
            'location',
            'color',
            'backgroundColor',
            'fontColor',
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['profile_image'].required = False
        self.fields['profile_cover'].required = False
        self.fields['profile_song'].required = False
        self.fields['profile_background'].required = False
        self.fields['hide_email'].required = False
        self.fields['bio'].required = False
        self.fields['location'].required = False
        self.fields['color'].required = False
        self.fields['backgroundColor'].required = False
        self.fields['fontColor'].required = False



    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image and profile_image.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError("The maximum file size that can be uploaded is 5MB")
        return profile_image

    def clean_profile_cover(self):
        profile_cover = self.cleaned_data.get('profile_cover')
        if profile_cover and profile_cover.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError("The maximum file size that can be uploaded is 5MB")
        return profile_cover

    def clean_profile_song(self):
        profile_song = self.cleaned_data.get('profile_song')
        if profile_song and profile_song.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError("The maximum file size that can be uploaded is 5MB")
        return profile_song

    def clean_profile_background(self):
        profile_background = self.cleaned_data.get('profile_background')
        if profile_background and profile_background.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError("The maximum file size that can be uploaded is 5MB")
        return profile_background