from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from testimonials.views import view_testimonials, testimonial_detail, add_testimonial, delete_testimonial


urlpatterns = [
    re_path(r'^testimonials/(?P<user_to_username>[\w.@+-]+)/$', view_testimonials, name='view_testimonials'),
    re_path(r'^testimonials/(?P<user_to_username>[\w.@+-]+)/(?P<testimonial_id>\d+)/$', testimonial_detail,
            name='testimonial_detail'),
    re_path(r'^addtestimonials/(?P<user_to_username>[\w.@+-]+)/$', add_testimonial, name='add_testimonial'),
    re_path(r'^testimonials/(?P<user_to_username>[\w.@+-]+)/delete/(?P<testimonial_id>\d+)/$', delete_testimonial,
            name='delete_testimonial'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
                  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
