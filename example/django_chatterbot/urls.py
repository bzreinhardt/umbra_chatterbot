from django.conf.urls import include, url
from django.contrib import admin

from django_chatterbot.api import ChatterBotView
from django_chatterbot.api import InputParserView
from django_chatterbot.api import InternalParserView


urlpatterns = [
    #url(
    #    r'^test/',
    #    ChatterBotView.as_view(),
    #    name="chatterbot",
    #),

    url(r'^external/',
    InputParserView.as_view(),
  	name="inputparser"),

    url(r'^internal/',
    InternalParserView.as_view(),
    name="inputparser"),

]
