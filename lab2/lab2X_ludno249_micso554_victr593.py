
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
with open('train.han') as f:
    for line in f:
        for i, char in enumerate(line):
            unigrams[char] = unigrams.get(char, 0) + 1
            if i > 0:
                bi_count += 1
                bigram = line[i-1] + char
                bigrams[bigram] = bigrams.get(bigram, 0) + 1
            uni_count += 1
        #print(bigrams)

v1_plus = 0
for word in unigrams:
    if word in wok:
        v1_plus += 1



k = v1_plus / V
print("MY K",k)

def prob_uni(word):
    return (unigrams[word] + k)/(uni_count + k*V)

def prob_bi(ctx, word):
    pass
    #return (bigrams[ctx+word] + k)/(bi_count + k*
