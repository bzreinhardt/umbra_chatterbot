from django.conf.urls import include, url
from django.contrib import admin

from django_chatterbot.api import ChatterBotView
from django_chatterbot.api import InputParserView


urlpatterns = [
    #url(
    #    r'^test/',
    #    ChatterBotView.as_view(),
    #    name="chatterbot",
    #),
    url(r'^$',
    	InputParserView.as_view(),
    	name="inputparser"),

]
