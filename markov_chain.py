__author__ = 'cmotevasselani'

import random
import os
import pprint

class MarkovChain:



    def __init__(self, percision):
        self.chain = {}
        self.percision = percision  # maybe rename ?
        self.model = []

    def add_to_model_from_file(self, filename):
        with open(filename, 'r') as input_text:
            for line in input_text:
                for word in line.split(' '):
                    self.model.append(word.rstrip("\n"))


    def create_chain_from_model(self):
        # found from: http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
        ngrams = zip(*[self.model[i:] for i in range(self.percision + 1)])
        for ngram in ngrams:
            key = ngram[:-1]
            value = ngram[-1]
            if key in self.chain:
                self.chain[key].append(value)
            else:
                self.chain[key] = [value]

    def generate_text_from_chain(self, text_len):
        start_word_index = random.randint(0, len(self.model) - self.percision)
        starting_key = tuple(self.model[start_word_index:start_word_index + self.percision])
        output_text = []
        for i in range(text_len):
            next_word = self.choose_word_from_key(starting_key)
            output_text.append(next_word + " ")
            starting_key = starting_key[1:] + tuple([next_word])
        pretty_print_array(output_text)

    def choose_word_from_key(self, key):
        words = self.chain[key]
        return random.choice(self.chain[key])


def pretty_print_array(text, words_per_line=10):
    split_text = chunks(text, words_per_line)
    for line in split_text:
        print ''.join(line) + "\n"


def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


markovChain = MarkovChain(percision=2)
for filename in os.listdir("data"):
    markovChain.add_to_model_from_file("data/" + filename)
markovChain.create_chain_from_model()
markovChain.generate_text_from_chain(100)
