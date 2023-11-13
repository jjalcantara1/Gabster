from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .forms import ContactForm
from .models import Contact

# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             message = form.cleaned_data['message']
#
#             # Save the contact form data to the database
#             Contact.objects.create(name=name, email=email, comment=message, subject=form.cleaned_data['subject'])
#
#             # Send email from the user's email address
#             send_mail(
#                 f'Contact Form Submission from {name}',
#                 message,
#                 email,  # Use the user's email as the 'from_email'
#                 ['HAUGabster@gmail.com'],  # Replace with your admin's email address
#                 fail_silently=False,
#             )
#             print(f'Sending email from: {email}')
#             return redirect('contact_success')  # Redirect to a "Thank you" page or desired location after submission
#     else:
#         form = ContactForm()
#
#     return render(request, 'contact/contact.html', {'form': form})
def contact_view(request):
    contacts = None

    if request.user.is_superuser:
        contacts = Contact.objects.all().order_by('created_at')

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        comment = request.POST.get("comment")
        query = Contact(name=name, email=email, subject=subject, comment=comment)
        query.save()
        success_message = "Your message has been sent successfully."
        return render(request, 'contact/contact.html', {'contacts': contacts, 'success_message': success_message})

    return render(request, 'contact/contact.html', {'contacts': contacts})
def send_email(request, subject, email, name):
    subject = ('Re:' + subject)
    email = email
    name = name
    print(subject)

    if request.method == "POST":
        print("request.POST")
        message = request.POST.get("message")
        message_data = {
            'name': name,
            'email': email,
            'comment': message,
            'subject': subject,

        }
        html_message = render_to_string('contact/email_template.html', message_data)
        plain_message = strip_tags(html_message)

        if subject and message and email:
            try:
                send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [email], html_message=html_message)
                return redirect('/')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
            return HttpResponse('Invalid form data')
    context = {
        'subject': subject,
        'email': email,
        'name': name,
    }
    return render(request, 'contact/email_response.html', context)
