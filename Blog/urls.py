from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *
urlpatterns = [
    path('home/',home),
    path('create/',create_post),
    path('post/<int:post_id>/',post_page),
    path('comment/<int:post_id>/',comment),
    path('signup/',signup),
    path('login/',signin),
    path('logout/',signout),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)