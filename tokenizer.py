import nltk
import re
import time
import io
import os
# import sgmllib
from sets import Set
# import itertools
from bs4 import BeautifulSoup
from nltk import stem

# class ExtractId(sgmllib.SGMLParser):
# 	def __init__(self, verbose=0):
# 		sgmllib.SGMLParser.__init__(self, verbose)
# 		self.id = []
# 		self.body = []
# 		self.current_id = ''
# 		self.current_text = ''
# 		self.data = None
# 		self.text_data = None

# 	def handle_data(self, data):
# 		if self.data is not None:
# 			self.data.append(data)

# 		if self.text_data is not None:
# 			self.text_data.append(data)

# 	def handle_starttag(self,tag, method, attrs):
# 		if tag == 'reuters':
# 			self.current_id = self.get_id_from_reuters(attrs)
# 		elif tag == 'text':
# 			self.current_text = self.text_data

# 	def handle_endtag(self, tag, method):
# 		if tag == 'reuters':
# 			self.id.append(self.current_id)
# 		elif tag == 'text':
# 			self.body.append(self.current_text)

# 	def start_reuters(self, attrs):
# 		self.data = []

# 	def end_reuters(self):
# 		self.data = None

# 	def start_text(self, attrs):
# 		self.text_data = []

# 	def end_text(self, attrs):
# 		self.body.append(''.join(self.text_data))
# 		self.text_data = None

# 	def get_id_from_reuters(self, attrs):
# 		for key, val in attrs:
# 			if key == 'newid':
# 				return val

# class ExtractText(sgmllib.SGMLParser):
# 	def __init__(self, verbose=0):
# 		sgmllib.SGMLParser.__init__(self, verbose)
# 		self.body = []
# 		self.data = None

# 	def handle_data(self, data):
# 		if self.data is not None:
# 			self.data.append(data)

# 	def start_text(self, attrs):
# 		self.data = []

# 	def end_text(self):
# 		self.body.append(''.join(self.data))
# 		self.data = None

def preProcessing(filename):

	f = open(filename, 'r')

	soup = BeautifulSoup(f.read())

	contentDict = dict()

	# parserId = ExtractId()

	# parserId.feed(data)

	# parserId.close()

	# for ids in parserId.id:
	# 	print ids

	# for bodies in parserId.body:
	# 	print bodies

	# # for textId in parserId.id:
	# # 	contentDict[textId] = 

	# parserText = ExtractText()

	# parserText.feed(data)

	# parserText.close()

	for texts in soup.findAll('reuters'):
		if texts.find('body'):
			contentDict[texts.get('newid')] = texts.find('body').text
		elif texts.find('text'):
			contentDict[texts.get('newid')] = texts.find('text').text


	stopwords = Set(["Reuters", "a", "about", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves"])

	numberRegex = re.compile('\d+')

	nonWordsRegex = re.compile('[^a-zA-Z0-9]+')

	numberRemover = Set()

	nonWordsRemover = Set()
	
	for key, value in contentDict.iteritems():
		allStemmed = []

		allWords = nltk.word_tokenize(value)

		for words in allWords:
			if numberRegex.match(words):
				numberRemover.add(words)
			elif nonWordsRegex.match(words):
				nonWordsRemover.add(words)


		allWords = Set(allWords)

		tokens = allWords - stopwords - numberRemover - nonWordsRemover

		stemmer=stem.PorterStemmer()

		for words in tokens:
			allStemmed.append(stemmer.stem(words))
			value = allStemmed

		print key
		print '\n'
		print value

		# print key
		# print value
		# print '\n\n\n\n'
		
	# for key, value in contentDict.iteritems():
		# print key
		# print '\n'
		# print value

	# for a in allStemmed:
	# 	print a



	# for words in allWords:
	# 	if numberRegex.match(words):
	# 		numberRemover.add(words)

	# allWords = Set(allWords)

	# tokens = allWords - stopwords - numberRemover

	# stemmed=[]

	# stemmer=stem.PorterStemmer()

	# for i in tokens:
	# 	stemmed.append(stemmer.stem(i))

	# return stemmed