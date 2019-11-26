import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

class TFIDF:

	def __init__(self):

		pass 

	def computeTF(self,wordDict, bagOfWords):
	    tfDict = {}
	    bagOfWordsCount = len(bagOfWords)
	    for word, count in wordDict.items():
	        tfDict[word] = count / float(bagOfWordsCount)
	    return tfDict

	def computeIDF(self,documents):
	    import math
	    N = len(documents)
	    
	    idfDict = dict.fromkeys(documents[0].keys(), 0)
	    for document in documents:
	        for word, val in document.items():
	            if val > 0:
	                idfDict[word] += 1
	    
	    for word, val in idfDict.items():
	        idfDict[word] = math.log(N / float(val))
	    return idfDict

	def computeTFIDF(self,tfBagOfWords, idfs):
	    tfidf = {}
	    for word, val in tfBagOfWords.items():
	        tfidf[word] = val * idfs[word]
	    return tfidf

	def run(self):

		documentA = 'the man went out for a walk'
		documentB = 'the children sat around the fire'

		bagOfWordsA = documentA.split(' ')
		bagOfWordsB = documentB.split(' ')

		uniqueWords = set(bagOfWordsA).union(set(bagOfWordsB))

		numOfWordsA = dict.fromkeys(uniqueWords, 0)

		#print (numOfWordsA)

		for word in bagOfWordsA:
		    numOfWordsA[word] += 1

		numOfWordsB = dict.fromkeys(uniqueWords, 0)

		for word in bagOfWordsB:
		    numOfWordsB[word] += 1

		tfA = self.computeTF(numOfWordsA, bagOfWordsA)
		tfB = self.computeTF(numOfWordsB, bagOfWordsB)


		print (tfA)

		idfs = self.computeIDF([numOfWordsA, numOfWordsB])


		tfidfA = self.computeTFIDF(tfA, idfs)
		tfidfB = self.computeTFIDF(tfB, idfs)
		df = pd.DataFrame([tfidfA, tfidfB])

		print (df)


def tfidfsk(doclist):

	vectorizer = TfidfVectorizer()
	vectors = vectorizer.fit_transform(doclist)
	feature_names = vectorizer.get_feature_names()
	dense = vectors.todense()
	denselist = dense.tolist()
	df = pd.DataFrame(denselist, columns=feature_names)

	return df

def main():

	#a= TFIDF()
	#print (a.run())

	documentA = 'the man went out for a walk'
	documentB = 'the children sat around the fire'
	tfidfsk([documentA,documentB])
	
if __name__ == '__main__':
	main()
