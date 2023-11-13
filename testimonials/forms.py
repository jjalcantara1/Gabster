from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from accounts.models import UserAccount
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['content']

    user_to = forms.ModelChoiceField(
        queryset=UserAccount.objects.all(),
        widget=forms.HiddenInput(),  # Use a hidden input field
        required=False  # Make the field non-required
    )

    # rating = forms.IntegerField(
    #     label='Rating',
    #     widget=forms.NumberInput(attrs={'type': 'number', 'min': 1, 'max': 5}),
    #     validators=[MinValueValidator(1), MaxValueValidator(5)]
    # )
    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')

        if not content:
            raise forms.ValidationError('Testimonial content is required.')
