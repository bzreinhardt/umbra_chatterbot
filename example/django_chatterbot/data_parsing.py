import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import treebank
from nltk.parse.generate import demo_grammar
from nltk import CFG
from stat_parser import Parser
from nltk.tree import ParentedTree

grammar = CFG.fromstring(demo_grammar)

class InputParser ():
    train_text_ = []
    custom_sent_tokenizer_ = []
    def __init__(self):

        self.train_text_ = state_union.raw("2005-GWBush.txt")
        self.custom_sent_tokenizer_ = PunktSentenceTokenizer(self.train_text_)

    def extract_parts(self, input):
        tokenized = self.custom_sent_tokenizer_.tokenize(input)
        try:
            for i in tokenized:
                words = nltk.word_tokenize(i)
                tagged = nltk.pos_tag(words)
            return tagged
        except Exception as e:
            print(str(e))

    def get_tree(self, input):
        parser = Parser()
        return parser.parse(input)

    def traverse(self,t):
        t = ParentedTree.convert(t)
        print t
        if t.height() == 3:
            cd = ''
            nns = ''
            for child in t:
                print "child is"
                print str(child.label())
                if str(child.label()) == 'CD':
                    cd = str(child.leaves())
                    print cd
                if str(child.label()) == 'NNS':
                    nns = str(child.leaves())
                    print nns
            if cd != '' and nns != '':
                print "found pair:"
                print cd
                print nns
            return
        else:
            for child in t:
                if t.height() > 2:
                    self.traverse(child)

    def find_noun_number_pair(self, input):
        tree = self.get_tree(input)
        self.traverse(tree)





