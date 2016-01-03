from django.views.generic.base import TemplateView


class ChatterBotAppView(TemplateView):
    template_name = "app.html"


class TestChatterBotView(TemplateView):
    template_name = "chat_interface.html"
