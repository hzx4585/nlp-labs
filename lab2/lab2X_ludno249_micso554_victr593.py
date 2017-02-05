# 腾 låt stå

d = 'src/'

# Dictionary for the chinese characters
char_map = {}

# Vocabulary
wok = set()

unigram_mem = {}
v1_bi_mem = {}


# Store all bigrams
unigrams = {}
bigrams = {}

uni_count = 0
bi_count = 0

# All words in vocabulary that have occured atleast once
v1_plus = set()

# Keep track of number of character tokens
N = 0

# Read in the charmap
with open(d + 'charmap') as f:
	for line in f:
		char, key = line.split()
		char_map[key] = char_map.get(key, []) + [char]

		wok.add(char)

print("Numbers of characters matching yi:", len(char_map['yi']), end="\n\n")

V = len(wok)

# Train the model
with open(d + 'train.han') as f:
	for line in f:
		# Add BOS and remove \n
		line = ['<BOS>'] + list(line[:-1])
		for i, char in enumerate(line):			
			# Unigram
			unigrams[char] = unigrams.get(char, 0) + 1
			
			# Bigram
			if i > 0:
				bigram = line[i - 1] + char
				bigrams[bigram] = bigrams.get(bigram, 0) + 1
			
				N += 1

			# V1_plus
			if char in wok:
				v1_plus.add(char)

k = len(v1_plus) / V

print("Training complete", end="\n\n")

## Methods for predicting characters
# Check how many unigrams begins with context
def begins_unigram(ctxt):
	if ctxt in unigram_mem:
		return unigram_mem[ctxt]

	cnt = 0
	for bi in bigrams:
		if ctxt == bi[:-1]:
			cnt += bigrams[bi]

	unigram_mem[ctxt] = cnt
	return cnt

# Check if bigrams starts with context, need to be in v1
def v1_plus_ctxt_bi(ctxt):
	cnt = 0

	if not ctxt in v1_plus:
		return 0

	if ctxt in v1_bi_mem:
		return v1_bi_mem[ctxt]

	for bi in bigrams:
		if ctxt == bi[:-1]:
			cnt += 1

	v1_bi_mem[ctxt] = cnt
	return cnt

# Lambda function, takes paramter u
def lumbdu_bi(u):
	cu = begins_unigram(u)
	if cu == 0:
		return 0
	return cu / (cu + v1_plus_ctxt_bi(u))

# Probability for unigram
def prob_uni(word):
	return (unigrams.get(word, 0) + k) / (N + k * V)

# Probabilty for bigram
def prob_bi(ctxt, word):
	lum = lumbdu_bi(ctxt)
	if(lum == 0):
		return prob_uni(word)
	return lum * bigrams.get(ctxt + word, 0) / begins_unigram(ctxt) +  (1 - lum) * prob_uni(word)

total_cnt = 0
total_hits = 0

lines = 0
# Open the test files and predict 
with open(d + 'test.han') as f_true, open(d + 'test.pin') as f_pred:
	for line in f_pred:
		predicted_line = ""
		lines += 1

		# Chinese characters, ignore newline
		true = f_true.readline()[:-1]
		
		# Input
		sentence = line.split()
		predicted_line = ['<BOS>']

		probabilities = []

		# For all tokens in the line
		for i, token in enumerate(sentence):
			highest_prob = 0

			# Handles the space
			highest_token = ' '

			# If the token is just a letter, include that one in the list as well
			single = [token] if len(token) == 1 else []

			# Try all possible characters for the tokens
			for china in char_map.get(token, []) + single:	
				tmp_prob = prob_bi(predicted_line[-1], china)
				if(tmp_prob >= highest_prob):
					highest_prob = tmp_prob
					highest_token = china

			# Add the most probable
			predicted_line.append(highest_token)
			probabilities.append("{0:.1f}".format(highest_prob*100))

		# Count precision and print out result
		predicted_line = predicted_line[1:]
		line_cnt = 0
		line_hits = 0
		for idx, char in enumerate(true):
			line_cnt += 1
			if char == predicted_line[idx]:
				line_hits += 1

		total_cnt += line_cnt
		total_hits += line_hits

		print("True:", true)
		print("Pred:", "".join(predicted_line))
		# Uncomment to get probabilities
		# print("Probabilities", " ".join(probabilities))
		print("Accuracy: {0:.2f}, tot accuracy: {1:.2f}, lines: {2}".format(100*line_hits/line_cnt, 100*total_hits/total_cnt, lines))

		print()

print("Total accuracy: {0:.2f}".format(100*total_hits/total_cnt))
