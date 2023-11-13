from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from verify_email.email_handler import send_verification_email
from accounts.forms import RegistrationForm, AccountAuthenticationForm, UserAccount
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from gabster_act import settings
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import ProfileUpdateForm


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'You are already authenticated as {user.email}.')
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # False since not yet verified
            user.save()

            send_verification_email(request, form)

            return render(request, 'accounts/email_ver_sent.html', {})
        else:
            context['registration_form'] = form

    return render(request, 'accounts/register.html', context)


# def send_activation_email(request, user):
#     current_site = get_current_site(request)
#     mail_subject = 'Activation link has been sent to your email id'
#     message = render_to_string('accounts/acc_active_email.html', {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user),
#     })
#     email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[user.email])
#
#     if email.send():
#         messages.success(request, 'Please confirm your email address to complete the registration')
#     else:
#         messages.error(request, 'Failed to send email confirmation. Please try again later.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.filter(pk=uid).first()
    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
    else:
        return HttpResponseBadRequest('Activation link is expired!')
    return render(request, 'accounts/email_ver_success.html', {})


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request, *args, **kwargs):
    # form = AccountAutheticationForm(request.POST)
    form = AccountAuthenticationForm()
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('profile', request.user.username)  # url required username, not sure bat ngayon lang nagerror

    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST:
        form = AccountAuthenticationForm(request.POST or None)
        print(form.non_field_errors())
        if form.is_valid():
            # email = request.POST['username']
            # password = request.POST['password']
            user = form.login(request)
            if user and user.is_active:
                login(request, user)
                # destination = kwargs.get('next')
                if destination:
                    return redirect(destination)
                return redirect('profile', request.user.username)
                # return redirect('profile_view')
            else:
                form = AccountAuthenticationForm()

                context['login_form'] = form

    return render(request, 'accounts/login.html', {'form': form})


def resend_email_ver(request):  # not included in package
    if request.method == 'POST':
        email = request.POST.get('email')  # get email from form

        user = UserAccount.objects.filter(email=email).first()  # look for user with the given email

        if user:
            if not user.is_email_verified:
                token = account_activation_token.make_token(user)  # makes the token
                user.update_user_joined_date()  # updates timestamp prior to request

                current_site = get_current_site(request)
                mail_subject = 'Resend Email Verification Mail'
                message = render_to_string('accounts/email_ver_resend_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token,  # use new token from token = account_activation_token.make_token(user)
                })
                to_email = user.email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                messages.success(request, 'A new verification email has been sent to your email address.')
                return render(request, 'accounts/email_ver_sent.html', {})
            else:
                return messages.error(request, 'Your email is already verified.')
        else:
            messages.error(request, 'Invalid email address.')

    return render(request, 'accounts/email_ver_sent.html')


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get('next'))
    return redirect


def email_ver_success(request):
    return render(request, 'accounts/email_ver_success.html', {})


def password_reset(request):
    return render(request, "accounts/password_reset.html", {})


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user  # Get the currently logged-in user
        user_to_delete = get_user_model().objects.get(pk=user.pk)  # Retrieve the user to be deleted by primary key

        # Verify that the request.user matches the user being deleted
        if user == user_to_delete:
            user_to_delete.delete()
            logout(request)
            return redirect('home')  # Redirect to the home page or any other desired page after account deletion
        else:
            # Handle the case where the request.user doesn't match the user to be deleted
            # You can display an error message or take appropriate action.
            return render(request, 'accounts/delete_account_error.html')

    return render(request, 'accounts/delete_account_confirmation.html')


@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile', username=request.user.username)  # Redirect to the current user's profile
    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'customization/profile_update.html', context)
