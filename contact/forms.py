from django import forms
from .models import Contact


# class Contact(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = ['name', 'email', 'subject', 'comment']

# class ContactForm(forms.Form):
#     name = forms.CharField(label='Your Name', max_length=100)
#     email = forms.EmailField(label='Your Email')
#     subject = forms.CharField(max_length=100)
#     message = forms.CharField(widget=forms.Textarea, label='Your Message')

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'comment']