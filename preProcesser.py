import nltk
import re
import sys
import json
from sets import Set
from nltk import stem
from collections import OrderedDict
reload(sys)
sys.setdefaultencoding('utf-8')

# f = open("index/index.txt", "w")

def preProcessing(documents,memorysize):

	postingsList = {}

	indexNumber = 00

	#Stop word set
	stopwords = Set(["Reuters", "reuters", "a", "about", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves"])

	#Number regex to remove numebrs
	numberRegex = re.compile('\d+')

	#Regex that removes non words and non numbers characters
	nonWordsRegex = re.compile('[^a-zA-Z0-9]+')

	#iniatiate empty set to store number tokens
	numberRemover = Set()

	#initiate empty set to store non words/numbers characters (i.e symbols and others)
	nonWordsRemover = Set()
	
	for key, value in documents.iteritems():
		
		#Tokenize
		allWords = nltk.word_tokenize(value)

		#Checks for numbers and symbols in tokens and adds them to a set
		for words in allWords:
			if numberRegex.match(words):
				numberRemover.add(words)
			elif nonWordsRegex.match(words):
				nonWordsRemover.add(words)

		#creates a set of all tokens
		allWords = Set(allWords)

		#Set operations to remove numbers, stop words and symbols
		terms = allWords - numberRemover - stopwords 

		for term in terms:
			if term in postingsList:
				#The term is already in the postings list => check if the key is already in the postings list
				if key not in postingsList[str(term)]:
					#if key is not in posting list, add it
					postingsList[str(term)].append(key)
			else:
				#if term not in postings list, initiate an empty array of document ids
				postingsList[str(term)] = [key]
				
				
		#initiate stemming
		# stemmer=stem.PorterStemmer()

		# for words in tokens:
		# 	allStemmed.append(stemmer.stem(words))
		# 	value = allStemmed

		#if size of postingsList gets bigger than memorysize chosen, writes to a new block
		if ((sys.getsizeof(postingsList)) > memorysize):
			sortedPostings = sorted(postingsList)
			sortedPostingsListTerms = OrderedDict()
			#sorting process for postingsList
			for item in sortedPostings:
				sortedPostingsListTerms[item] = postingsList[item]
			postingsList = sortedPostingsListTerms
			sortedPostingsListTerms = {}

			#for reading later, have to have this otherwise the postingsList are not sorted in the last index file
			if indexNumber < 10:
				formatedIndexNumber = '%02d' % indexNumber
			else:
				formatedIndexNumber = str(indexNumber)

			with open('index/index-' + formatedIndexNumber + '.json', 'w') as theFile:
				indexNumber+=1
				json.dump(postingsList, theFile)
			postingsList = {}	