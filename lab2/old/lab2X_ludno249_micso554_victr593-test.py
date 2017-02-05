# 腾 låt stå

# Dictionary for the chinese characters
char_map = {}

# Vocabulary
wok = set()

in_char_map = set()
# Read in the charmap
with open('charmap') as f:
	for line in f:
		char, key = line.split()
		wok.add(char)
		in_char_map.add(char)
		char_map[key] = char_map.get(key, []) + [char]

print("Numbers of characters matching yi:", len(char_map['yi']))

unigrams = {}
bigrams = {}
trigrams = {}

uni_count = 0
bi_count = 0
tri_count = 0

with open('train.han') as f:
	for line in f:
		
		# BOS
		line = ['<BOS>'] + list(line[:-1])
		for i, char in enumerate(line):
		
			# Vocabulary
			wok.add(char)

			# Unigram
			unigrams[char] = unigrams.get(char, 0) + 1
			uni_count += 1

			# Bigram
			if i > 0:
				bigram = line[i-1] + char
				bigrams[bigram] = bigrams.get(bigram, 0) + 1
				bi_count += 1
		
			# Trigram
			if i > 1:
				trigram = line[i-2] + line[i-1] + char
				trigrams[trigram] = trigrams.get(trigram, 0) + 1
				tri_count += 1

V = len(wok)
print("Created grams")

v1_plus = set()
for word in unigrams:
	if word in wok:
		v1_plus.add(word)
	#if word in 
	#pass

v1_plus_cnt = len(v1_plus)

k = v1_plus_cnt / V
N = uni_count

print("K IS ",k)

def prob_uni(word):
	return (unigrams.get(word, 0) + k) / (N + k * V)

unigram_mem = {}
def begins_unigram(ctxt):
	#print("CTXT", ctxt)
	ctxt = "".join(ctxt)
	if ctxt in unigram_mem:
		return unigram_mem[ctxt]

	cnt = 0
	for bi in bigrams:
		if ctxt == bi[:-1]:
			cnt += bigrams[bi]

	unigram_mem[ctxt] = cnt
	return cnt

bigram_mem = {}
def begins_bigram(ctxt):
	ctxt = "".join(ctxt)
	if ctxt in bigram_mem:
		return bigram_mem[ctxt]

	cnt = 0
	for tri in trigrams:
		if ctxt == tri[:-1]:
			cnt += trigrams[tri]

	bigram_mem[ctxt] = cnt
	return cnt

v1_bi_mem = {}
def v1_plus_ctxt_bi(ctxt):
	cnt = 0
	ctxt = "".join(ctxt)
	if ctxt not in v1_plus:
		return 0

	if ctxt in v1_bi_mem:
		return v1_bi_mem[ctxt]

	for bi in bigrams:
		if ctxt == bi[:-1]:
			cnt += 1
	v1_bi_mem[ctxt] = cnt
	return cnt

#v1_mem = {}
v1_tre_mem = {}
def v1_plus_ctxt_tri(ctxt):
	cnt = 0
	ctxt = "".join(ctxt)
	if ctxt not in v1_plus:
		return 0

	if ctxt in v1_tri_mem:
		return v1_tri_mem[ctxt]

	for tri in trigrams:
		if ctxt == tri[:-1]:
			cnt += 1
	v1_tri_mem[ctxt] = cnt
	return cnt

# Lambda function, takes paramter u
def lumbdu_bi(u):
	#print("u", u)
	cu = begins_unigram(u)
	if cu == 0:
		return 0
	return cu / (cu + v1_plus_ctxt_bi(u))

# Lambda function, takes paramter u
def lumbdu_tri(u):
	cu = begins_bigram(u)
	if cu == 0:
		return 0
	return cu / (cu + v1_plus_ctxt_tri(u))

def prob_bi(ctxt, word):
	ctxt = ctxt[0]
	lum = lumbdu_bi(ctxt)
	if(lum == 0):
		return prob_uni(word)
	return lum * bigrams.get(ctxt + word, 0) / begins_unigram(ctxt) +  (1 - lum) * prob_uni(word)

def prob_tri(ctxt, word):
	return prob_bi(ctxt[0], word)

	if len(ctxt) < 2:
		return prob_bi(ctxt, word)
	#ctxt = ctxt[0]
	str_ctxt = "".join(ctxt)
	#return prob_bi(ctxt, word)
	lum = lumbdu_tri(str_ctxt)
	if(lum == 0):
		return prob_bi(ctxt[1:], word)
		#return prob_uni(word)
	return lum * trigrams.get(str_ctxt + word, 0) / begins_bigram(ctxt) +  (1 - lum) * prob_bi(ctxt[1:], word)

total_cnt = 0
total_hits = 0

lines = 0
# Open the test files
with open('test.han') as f_true, open('test.pin') as f_pred:
	for line in f_pred:
		predicted_line = ""
		lines += 1

		# Chinese characters, ignore newline
		true = f_true.readline()[:-1]
		
		# Input
		sentence = line.split()
		predicted_line = ['<BOS>']

		# For all tokens in the line
		for i, token in enumerate(sentence):
			highest_prob = 0

			# Handles the space
			highest_token = ' '

			# If the token is just a letter, include that one in the list as well
			single = [token] if len(token) == 1 else []
			for china in char_map.get(token, []) + single:	
		#		print(predicted_line[-3:])
				tmp_prob = prob_tri(predicted_line[-1:], china)
				if(tmp_prob >= highest_prob):
					highest_prob = tmp_prob
					highest_token = china

			predicted_line.append(highest_token)

		# Count precision
		predicted_line = predicted_line[1:]
		line_cnt = 0
		line_hits = 0
		for idx, char in enumerate(true):
			line_cnt += 1
			
			if char == predicted_line[idx]:
				line_hits += 1

		print("True:", true)
		print("Pred:", "".join(predicted_line))
		print("Accuracy: {0:.2f}, Lines: {1}".format(100*line_hits/line_cnt, lines))

		total_cnt += line_cnt
		total_hits += line_hits
		print()

print("Total accuracy: {0:.2f}".format(100*total_hits/total_cnt))
