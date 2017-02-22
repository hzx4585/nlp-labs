'''
    ./word2vec -train oanc.txt -output trained_model_oanc.bin -cbow 0 -binary 1
    https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/models/word2vec.py
'''

from random import randint
#from gensim import corpora
import gensim


#model = gensim.Word2Vec.load_word2vec_format('trained_model_oanc.bin', binary=True)  # C binary format


def find_synonym(word, candidates):
    '''
    Input: word to find synonyms to

    Return: the index of the correct candidate
    '''
    return randint(0, 3)

synonyms = []
with open('res/toefl.txt') as f:
    for line in f:
        synonyms.append(line.split())

accuracy = []
for s in synonyms:
    word = s[0]
    gold = int(s[1])
    candidates = s[2:]

    accuracy.append(gold == find_synonym(word, candidates))


print("Accuracy: {0:.2f}".format( 100 * sum(accuracy) / len(accuracy) ))
