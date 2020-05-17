from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *
urlpatterns = [
    path('',landing),
    path('home/',home),
    path('create/',create_post),
    path('post/<int:post_id>/',post_page),
    path('comment/<int:post_id>/',comment),
    path('signup/',signup),
    path('login/',signin),
    path('logout/',signout),
    path('delete/<int:post_id>/',delete),
    path('like/<int:post_id>/',like),
    path('edit/<int:post_id>/',edit_post),
    path('delete_comment/<int:comment_id>/<int:post_id>/',delete_comment),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)