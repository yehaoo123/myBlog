"""myBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.urls import re_path
from apps.backend import views as backend_view

urlpatterns = [
    path('login/', backend_view.login.as_view()),
    path('check_code/', backend_view.checkCode),
    re_path('articles/(?P<page>\d*)/?', backend_view.backendArticles.as_view()),
    re_path('edit-(?P<id>\d+)/', backend_view.articlesEdit),
    path('delete/', backend_view.articleDelete),
    path('labels/', backend_view.backendLabel.as_view()),
    path('publish/', backend_view.backendPublish.as_view()),
    path('exit/', backend_view.exit.as_view()),
    path('', backend_view.user.as_view()),
    path('article_imgs/', backend_view.article_imgs),
]
