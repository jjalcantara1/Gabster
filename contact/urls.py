from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from contact.views import *

urlpatterns = [
    path('contact/', contact_view, name='contact'),
    path('send_email/<str:subject>/<str:email>/<str:name>/', send_email, name='send_email'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
                  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
