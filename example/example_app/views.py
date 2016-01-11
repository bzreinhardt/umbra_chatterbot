from django.views.generic.base import TemplateView


class ChatterBotAppView(TemplateView):
    template_name = "app.html"


class TestChatterBotView(TemplateView):
    template_name = "chat_interface.html"

class InputView(TemplateView):
    template_name = "text_parsing.html"
    #def post(self, request, *args, **kwargs):
    #    print ("got at thing")
