from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from .import views
from .views import *



urlpatterns = [
    path('comment_post/<int:post_id>/', comment_post, name='comment_post'),
    path('profile/<str:username>/<int:post_id>/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
                  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
