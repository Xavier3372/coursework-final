import nltk
from nltk.corpus import words
from nltk.metrics.distance import edit_distance #The edit distance is the number of characters that need to be substituted, inserted, or deleted, to transform s1 into s2.
import pandas as pd

nltk.download('words')

spelling_words = pd.Series(words.words())

def autoCorrect(wd): #Checks edit distance, smaller edit distance = closest word match
    right_words = []
    nltk.download('words')
    spelling_words = pd.Series(words.words())
    

    distance = ((edit_distance(wd, s), s) for s in spelling_words if len(s) == len(wd) and s[0] == wd[0])
    closest = min(distance) # is a tuple
    right_words.append(closest[1]) #appends the corrected word
    return right_words




