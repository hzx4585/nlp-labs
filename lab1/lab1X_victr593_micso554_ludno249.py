import numpy as np

# Maximum Entropy Classifier

def softmax(X):
	"""Computes the softmax function for the specified batch of data.

	This uses a common trick to improve numerical stability; this trick is
	explained here:

	http://stackoverflow.com/a/39558290
	"""
	E = np.exp(X - np.max(X, axis=1, keepdims=True))
	return E / E.sum(axis=1, keepdims=True)

def minibatches(X, Y, batch_size):
	"""Yields minibatches from the specified X and Y matrices.

	Instead of computing updates on the complete data, it is a good idea
	to only compute them on parts of the data; these parts are called
	minibatches. This function randomly splits the input data into
	minibatches of the specified size.
	"""
	m = X.shape[0]
	n_batches = int(np.floor(m / batch_size))
	random_indices = np.random.permutation(np.arange(m))
	for i in range(n_batches):
		batch_indices = np.arange(i * batch_size, (i + 1) * batch_size)
		batch_indices = random_indices[batch_indices]
		yield X[batch_indices], Y[batch_indices]

class MaxentClassifier(object):

	def __init__(self, n_features, n_classes):
		self.W = np.zeros((n_features, n_classes))

	def p(self, X):
		"""Returns the class probabilities for the given input."""
		tmp = X.dot(self.W)
		if(tmp[0] < tmp[1]):
			return 1
		else:
			return 0

		return softmax(X.dot(self.W))

	def predict(self, X):
		"""Returns the most probable class for the given input"""
		res = []
		for review in X:
			res.append(self.p(review))
		return res

	@classmethod
	def train(cls, X, Y, n_epochs=1, batch_size=1, eta=0.01, reg=0.1):
		classifier = cls(X.shape[1], Y.shape[1])
		for i in range(n_epochs):
			for X_hat, Y_hat in minibatches(X, Y, batch_size):
				a = softmax(X_hat.dot(classifier.W))
				b = Y_hat - a
				c = X_hat.T.dot(b)
				d = reg * classifier.W
				e = eta * (c - d)

				classifier.W = classifier.W + e

		return classifier

def build_w2i(data):
	"""Builds a word index, a mapping from words to integers.

	In order to represent a review as a NumPy vector, we need to assign to
	each word in our training set a unique integer index which will give
	us the component in the vector that is 1 if the corresponding word is
	present in the review, and 0 otherwise.
	"""
	w2i = {}
	cnt = 0
	for review in data:
		for word in review['text'].split():
			if word not in w2i:
				w2i[word] = cnt
				cnt += 1

	return w2i

def featurize(data, w2i):
	"""Converts review data into matrix format

	The argument w2i is a word index, as described above. The function
	should return a pair of NumPy matrices X, Y, where X is an N-by-F
	matrix (N: number of instances in the data, F: number of
	features), and where Y is an N-by-K matrix (K: number of classes).
	"""
	X = np.zeros(shape=(len(data), len(w2i)))
	Y = np.zeros(shape=(len(data), 2))
	for cnt, review in enumerate(data):
		tdlist = [0]*len(w2i)
		for word in review['text'].split():
			if word in w2i:
				tdlist[w2i[word]] = 1
		X[cnt,:] = tdlist

		pos = review['polarity'] == "pos"
		Y[cnt,:] = [int(pos), int(not pos)]

	return X, Y

if __name__ == "__main__":
	import json
	import sys

	# Seed the random number generator to get reproducible results
	np.random.seed(42)

	# Load the training data and featurize it
	with open(sys.argv[1]) as f:
		training_data = list(json.load(f))
	w2i = build_w2i(training_data[:])
	X, Y = featurize(training_data, w2i)

	# Train the classifier
	classifier = MaxentClassifier.train(X, Y, 5, 18, 0.01, 0.1)

	# Compute the accuracy of the trained classifier on the test data
	with open(sys.argv[2]) as f:
		test_data = list(json.load(f))
	X, Y = featurize(test_data, w2i)
	print("Prediction accuracy: {0}%". format(100*np.mean(classifier.predict(X) == np.argmax(Y, axis=1))))
