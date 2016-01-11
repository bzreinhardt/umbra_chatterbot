"""django_chatterbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from example_app.views import ChatterBotAppView
from example_app.views import TestChatterBotView
from example_app.views import InputView


urlpatterns = [
    #url(r'^$', ChatterBotAppView.as_view()),
    #url(r'^test/', TestChatterBotView.as_view()),
    #url(r'^chatterbot/', include('django_chatterbot.urls')),
    #url(r'^api/chatterbot/', include('django_chatterbot.urls', namespace='chatterbot')),
    #url(r'^test/', include('django_chatterbot.urls')),
    url(r'^llama',InputView.as_view()),
    url(r'^input/', include('django_chatterbot.urls')),
    
]

