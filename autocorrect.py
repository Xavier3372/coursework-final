from english_words import english_words_set
# The edit distance is the number of characters that need to be substituted, inserted, or deleted, to transform s1 into s2.
from nltk.metrics.distance import edit_distance



def autoCorrect(wd):  
    # Find number of edits to convert current word into different possible correct words
    distance = ((edit_distance(wd, s), s) 
                for s in english_words_set)
    # Find word that requires least number of edits to convert from current word to correct word
    closest = min(distance)
    wordString = ''
    # Assign correct word to string
    wordString += closest[1]
    # returns string
    return wordString

