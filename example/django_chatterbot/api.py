from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
### NLP Stuff
import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

train_text = state_union.raw("2005-GWBush.txt")
custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

def process_input(input):
    tokenized = custom_sent_tokenizer.tokenize(input)
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
        return tagged
    except Exception as e:
        print(str(e))

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
        input_statement = request.POST.get('text')
        parsed_input = process_input(input_statement)
        dic = nlp_list_to_dict(parsed_input)
        response = JsonResponse(dic)
        return response

