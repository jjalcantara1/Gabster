from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from .import views
from .views import *



urlpatterns = [
    re_path(r'^createpost/(?P<username>[\w.@+-]+)/$', create_post, name='create_post'),
    re_path(r'^profile/(?P<username>[\w.@+-]+)/(?P<post_id>\d+)/$', post_detail, name='post_detail'),
    path('profile/<str:username>/<int:post_id>/like/', like, name='like'),
    path('get-likes/<str:username>/<int:post_id>/', views.get_likes, name='get_likes'),
    path('profile/<str:username>/<int:post_id>/likedby', likedby, name='likedby'),
    path('profile/<str:username>/<int:post_id>/delete/', delete_post, name='delete_post'),

]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
                  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
