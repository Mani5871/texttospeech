from django.contrib import admin
from django.urls import path
from home import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('file/', views.myfile, name = "file"),
    path('', views.index, name = "home"),
    path('words/', views.words, name = "words"),
    path('files/', views.files, name = "files"),
    path('signin/', views.signin, name = "signin"),
    path('signup/', views.signup, name = "signup"),
    path('signout/', views.signout, name = "signout")
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    