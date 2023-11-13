from urllib import request

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import authenticate
from django.forms import EmailField
from django.forms.utils import ErrorList
from accounts.models import UserAccount
from django.contrib.auth import get_user_model

UserAccount = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255,
                             help_text="An email address is required. Please add a valid email address.")

    class Meta:
        model = UserAccount
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = UserAccount.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email} is already in use.')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            account = UserAccount.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")


class AccountAuthenticationForm(forms.Form):
    username = forms.CharField(label='Username or Email', widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    #
    # class Meta:
    #     model = UserAccount
    #     fields = ('email', 'password')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            user = authenticate(email=username, password=password)

        if not user or not user.is_active:
            raise forms.ValidationError("Invalid login.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            user = authenticate(email=username, password=password)

        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['profile_image', 'profile_cover', 'profile_song', 'profile_background', 'bio', 'location', 'color',
                  'backgroundColor', 'fontColor']


class ColorPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['color']


class BackgroundColorPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['backgroundColor']


# class FontPreferenceForm(forms.ModelForm):
#     FONT_CHOICES = (
#         ('Young Serif', 'Young Serif'),
#         ('Roboto Slab', 'Roboto Slab'),
#         ('Noto Sans JP', 'Noto Sans JP'),
#         ('Yuji Hentaigana Akari', 'Yuji Hentaigana Akari'),
#     )
#     font_preference = forms.ChoiceField(
#         choices=FONT_CHOICES,
#         required=True,
#         widget=forms.Select(attrs={'class': 'form-control'}),
#     )
#
#     class Meta:
#         model = UserAccount
#         fields = ['font_preference']


class FontColorPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['fontColor']
