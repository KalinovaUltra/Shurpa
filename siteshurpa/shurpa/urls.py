from django.conf.urls.static import static

from siteshurpa import settings
from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),#http://127.0.0.1:8000
    path('about/', views.about, name='about'),
    path('otziv/', views.otziv, name='otziv'),
    path('test/', views.test, name='test'),
    path('post/<slug:post_slug>/',  views.show_post, name='post'),
    path('category/<slug:cat_slug>/',  views.show_category, name='category'),
    path('tag/<slug:tag_slug>/',  views.show_tag_postlist, name='tag'),
    path('chat/', views.chat_with_gpt, name='chat'),
    path('addpage/', views.addpage, name='addpage'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
