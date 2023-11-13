from django.urls import path, re_path
from customization.views import update_profile

from customization import views

urlpatterns = [
    path('update_profile/', update_profile, name='update_profile'),
]