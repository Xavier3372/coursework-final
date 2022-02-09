from english_words import english_words_set
# The edit distance is the number of characters that need to be substituted, inserted, or deleted, to transform s1 into s2.
from nltk.metrics.distance import edit_distance


def autoCorrect(wd):  # Checks edit distance, smaller edit distance = closest word match
    distance = ((edit_distance(wd, s), s)
                for s in english_words_set)
    closest = min(distance)  # is a tuple
    wordString = ''
    wordString += closest[1]
    return wordString


