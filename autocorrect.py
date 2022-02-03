import nltk
from nltk.corpus import words
from nltk.metrics.distance import edit_distance #The edit distance is the number of characters that need to be substituted, inserted, or deleted, to transform s1 into s2.
import pandas as pd

nltk.download('words')

spelling_words = pd.Series(words.words())

wd = ['mbther', 'fbther']

def autoCorrect(wd, spelling_words): #Checks edit distance, smaller edit distance = closest word match
    right_words = []
    
    for i in wd:
        distance = ((edit_distance(i, s), s) for s in spelling_words if len(s) == len(i) and s[0] == i[0])
        closest = min(distance) # is a tuple
        right_words.append(closest[1]) #appends the corrected word
    return right_words

print(autoCorrect(wd, spelling_words))

