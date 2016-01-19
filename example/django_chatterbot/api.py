from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
### NLP Stuff
import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from data_parsing import InputParser



chatterbot = ChatBot(
    'Example ChatterBot',
    io_adapter="chatterbot.adapters.io.JsonAdapter"
)

def nlp_list_to_dict(input_list):
    out = dict()
    out['text'] = ''
    for item in input_list:
        out['text'] = out['text'] + 'word: ' + item[0] + ' part of speech: ' + item[1] + '\n'
    return out
# TODO(breinhardt) - move this in to a library


chatterbot.train([
    "Hi",
    "Hello",
    "How are you?",
    "I am good.",
    "That is good to hear.",
    "Thank you",
    "You are welcome.",
])


class ChatterBotView(View):

    def get(self, request, *args, **kwargs):
        data = {
            'detail': 'You should make a POST request to this endpoint.'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

    def post(self, request, *args, **kwargs):
        input_statement = request.POST.get('text')
        print("chatterbot triggered")
        response_data = chatterbot.get_response(input_statement)

        return JsonResponse(response_data)


class InputParserView(View):
    def post(self, request, *args, **kwargs):
        input = request.POST.get('text')
        # Try doing raw input parsing
        parser = InputParser()
        numbered_pairs = parser.find_noun_number_pair(input)
        print "numbered pairs "
        print numbered_pairs

        response_text = ""
        if len(numbered_pairs) > 0:
            #register the numbered pair in the database
            response_text = "okay, you did " 
            for pair in numbered_pairs:
                response_text = response_text + \
                str(pair['cd'][0]) + \
                " " + str(pair['nns'][0]) + " and "
        else:
            response_text = "defaulting to chatterbot"
            #response_text = chatterbot.get_response(input)
        response = {}
        response['text'] = response_text
        response = JsonResponse(response)
        return response

class InternalParserView(View):
    def post(self, request, *args, **kwargs):
        input = request.POST.get('text')
        parser = InputParser()
        log = parser.find_key_value_pair(input)
        response_text = ""
        if len(log) > 0:
            # register the numbered pair in the database
            response_text = "logging "
            for key in log:
                response_text = response_text + \
                    str(key) + \
                    " : " + str(log[key])
        # log pair to db
        response = {}
        response['text'] = response_text
        response = JsonResponse(response)
        return response

