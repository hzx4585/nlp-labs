'''
    ./word2vec -train oanc.txt -output trained_model_oanc.bin -cbow 0 -binary 1
'''

import gensim

file1 = 'word2vec/trunk/trained_model_oanc.bin'
file2 = 'word2vec/trunk/trained_model_wiki.bin'

def find_synonym(model, word, candidates):
    '''
    Input: word to find synonyms to

    Return: the index of the correct candidate
    '''
    best_score = -1
    best_idx = -1
    for idx, candidate in enumerate(candidates):
        try:
            tmp_score = model.similarity(word, candidate)
        except:
            tmp_score = -1
        if tmp_score > best_score:
            best_score = tmp_score
            best_idx = idx

    return best_idx

def main(filename):
    print("Using file:", filename)
    model = gensim.models.Word2Vec.load_word2vec_format(filename, binary=True)
    synonyms = []
    with open('res/toefl.txt') as f:
        for line in f:
            synonyms.append(line.split())

    accuracy = []
    for s in synonyms:
        word = s[0]
        gold = int(s[1])
        candidates = s[2:]

        accuracy.append(gold == find_synonym(model, word, candidates))

    print("Accuracy: {0:.2f}".format( 100 * sum(accuracy) / len(accuracy) ))

main(file1)
main(file2)
