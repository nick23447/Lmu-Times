"""
Author: Nicholas Laus
Sources: Word List from slushman on github
Date: 4/9/24
Desctiption: Generates a random five letter word
"""


from random import *
from wordle_list import words


def get_random_word():

    word_list = words

    def word_generator(word_list):
        num = randint(0, len(word_list) - 1)
        return word_list[num]

    wordle_word = word_generator(words)

    return wordle_word
