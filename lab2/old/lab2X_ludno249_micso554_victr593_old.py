# 腾 låt stå
import time
char_map = {}
wok = set()

with open('charmap') as f:
    for line in f:
        char, key = line.split()
        wok.add(char)
        char_map[key] = char_map.get(key, []) + [char]

print("Numbers of characters matching yi:", len(char_map['yi']))

V = len(wok)

bigrams = {}
unigrams = {}
uni_count = 0
bi_count = 0
count = 0
t_0 = time.time()

with open('train.han') as f:
    for line in f:
        for i, char in enumerate(line):
            # Handle UNK
            if char in wok:
                corr_char = char
            else:
                corr_char = '<UNK>'

            unigrams[corr_char] = unigrams.get(corr_char, 0) + 1

            if i == 0:
                hej = '<BOS>'
            else:
                hej = line[i - 1]
            uni_count += 1
            bi_count += 1

            bigram = hej + corr_char
            bigrams[bigram] = bigrams.get(bigram, 0) + 1

v1_plus = set()
for word in unigrams:
    if word in wok:
        v1_plus.add(word)

v1_plus_cnt = len(v1_plus)

k = v1_plus_cnt / V
N = uni_count

def prob_uni(word):
    return (unigrams.get(word, 0) + k) / (N + k * V)

unigram_mem = {}
def begins_unigram(ctxt):
    if ctxt in unigram_mem:
        return unigram_mem[ctxt]

    cnt = 0
    for bi in bigrams:
        if ctxt == bi[:-1]:
            cnt += bigrams[bi]
    unigram_mem[ctxt] = cnt
    return cnt

v1_mem = {}
def v1_plus_ctxt_prick(ctxt):
    cnt = 0
    if ctxt not in v1_plus:
        return 0

    if ctxt in v1_mem:
        return v1_mem[ctxt]

    for bi in bigrams:
        if ctxt == bi[:-1]:
            cnt += 1
    v1_mem[ctxt] = cnt
    return cnt

def lumbdu(u):
    cu = begins_unigram(u)
    if cu == 0:
        return 0
    return cu / (cu + v1_plus_ctxt_prick(u))

def prob_bi(ctxt, word):
    lum = lumbdu(ctxt)
    if(lum == 0):
        return prob_uni(word)
    return lum * bigrams.get(ctxt + word, 0) / begins_unigram(ctxt) +  (1 - lum) * prob_uni(word)

total_cnt = 0
hits = 0
lines = 0
# Open the test files
with open('test.han') as f_true, open('test.pin') as f_pred:
    for line in f_pred:
        predicted_line = ""
        lines += 1

        true = f_true.readline()

        sentence = ['<BOS>']+line.split() + ['\n']
        # For all tokens in the line
        for i, token in enumerate(sentence):
            if i ==  0:
                prev_china = '<BOS>'
                continue

            highest_prob = 0
            # Handles the space
            highest_token = ' '

            # Finds the best chinese character with the previous character
            single = [token] if len(token) == 1 else []
            for china in char_map.get(token, []) + single:
                tmp_prob = prob_bi(prev_china, china)
                if(tmp_prob >= highest_prob):
                    highest_prob = tmp_prob
                    highest_token = china

            prev_china = highest_token

            if(true[i-1] == highest_token):
                hits += 1

            total_cnt += 1

            predicted_line += highest_token

        # Print the progress
        print("True:", true, end="")
        print("Pred:", predicted_line, end="")
        print("Accuracy: {0:.5f}, Lines: {1}    ".format(100*hits/total_cnt, lines))
        print()

print("Total accuracy: {0:.2f}".format(100*hits/total_cnt))
