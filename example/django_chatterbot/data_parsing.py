import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import treebank
from nltk.parse.generate import demo_grammar
from nltk import CFG
from stat_parser.parser import Parser
from nltk.tree import ParentedTree
import logging

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
        result = []
        cd = ''
        nns = ''
        print "subtree = "
        print t
        for child in t:
            print "child = "
            print child
            if str(child.label()) == 'CD':
                cd = child.leaves()
            if str(child.label()) == 'NNS':
                nns = child.leaves()
            if cd != '' and nns != '':
                print "found pair:"
                pair = {}
                pair['cd'] = cd
                pair['nns'] = nns
                # stick things in a dictionary
                print pair
                result.append(pair)
            if child.height() > 2:
                    #append the returned dictionary to this dictionary
                result.extend(self.traverse(child))
        return result

    def find_noun_number_pair(self, input):
        tree = self.get_tree(input)
        output = self.traverse(tree)
        return output

    #assumes an input in the form "foo:bar"
    def find_key_value_pair(self, input):
        split = input.split(':')
        #assume the first thing is the key and
        # everything else goes with it
        log = {}
        log[split[0]] = split[1:]
        return log








