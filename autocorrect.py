import nltk
from english_words import english_words_set
# The edit distance is the number of characters that need to be substituted, inserted, or deleted, to transform s1 into s2.
from nltk.metrics.distance import edit_distance
import pandas as pd
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


def autoCorrect(wd):  # Checks edit distance, smaller edit distance = closest word match
    right_words = []

    distance = ((edit_distance(wd, s), s)
                for s in english_words_set if len(s) == len(wd) and s[0] == wd[0])
    closest = min(distance)  # is a tuple
    right_words.append(closest[1])  # appends the corrected word
    wordString = ''
    for _ in right_words:
        wordString += _
    return wordString
