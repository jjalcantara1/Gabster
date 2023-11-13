"""
URL configuration for gabster_act project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path  # para mainclude ung views ng posts app
from django.conf import settings
from django.conf.urls.static import static


from accounts.views import login_view, register_view, logout_view
from .views import *
from accounts import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('gasbter_admin/', include('admin_custom.urls')),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('contact.urls')),
    path('', include('comment.urls')),
    path('', include('customization.urls')),
    path('', include('Post.urls')),
    path('', include('testimonials.urls')),


    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    re_path(r'^profile/(?P<username>[\w.@+-]+)/$', profile_view, name='profile'),

    path('verification/', include('verify_email.urls')),
    path('email_verification_sent/', views.resend_email_ver, name='email_verification_sent'),
    path('email_verification_success/', views.email_ver_success, name='email_verification_success'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),

    path('search/', search, name='search'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name='reset_password'),
    path('password_reset_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
                  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
