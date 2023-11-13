from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.utils import timezone

def is_token_expired(current_timestamp):
    now = timezone.localtime()
    return now > current_timestamp + timezone.timedelta(seconds=10)  # set to expire in 10 seconds

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.pk) + user.email + six.text_type(user.is_active) +
                six.text_type(timestamp)
        )

account_activation_token = AccountActivationTokenGenerator()

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

            # Send email verification link to the user
            token = account_activation_token.make_token(user)
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'accounts/email_ver_sent.html', {})
        else:
            context['registration_form'] = form

    return render(request, 'accounts/register.html', context)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.filter(pk=uid).first()
    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None:
        current_timestamp = timezone.localtime()  # get current timestamp
        token_expired = is_token_expired(current_timestamp)  # check if token is expired

        # Print the server timestamp
        print("Server Timestamp:", current_timestamp)

        if not token_expired:
            user.is_active = True
            user.is_email_verified = True
            user.save()
            return render(request, 'accounts/email_ver_success.html', {})
        else:
            if token_expired:
                return HttpResponseBadRequest('Activation link is expired!')
            return HttpResponseBadRequest('Activation link is invalid or expired!')
    else:
        return HttpResponseNotFound('Activation link is invalid!')
