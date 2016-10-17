import nltk
import re
import sys
from sets import Set
from nltk import stem
reload(sys)
sys.setdefaultencoding('utf-8')

f = open("index/index.txt", "w")

def preProcessing(documents):

	postingsList = {}


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

		#Checks for numbers and non words/numbers characters in tokens and adds them to a set
		for words in allWords:
			if numberRegex.match(words):
				numberRemover.add(words)
			elif nonWordsRegex.match(words):
				nonWordsRemover.add(words)

		#creates a set of all tokens in lowercase
		allWords = Set(allWords)

		#Set operations to remove numbers, stop words and non words/numbers characters
		terms = allWords - stopwords - numberRemover - nonWordsRemover

		for term in terms:
			if term in postingsList:
				#The term is already in the postings list => check if the key is already in the postings list
				if key not in postingsList[term]:
					#if key is not in posting list, add it
					postingsList[term].append(key)
			else:
				#if term not in postings list, initiate an empty array of document ids
				postingsList[term] = [key]
		
	for key,value in postingsList.iteritems():
		f.write(str(key) + ":" + str(value) + '\n')

	# for key, value in sorted(postingsList).iteritems():
	# 	print key

	

	# for key, value in postingsList.iteritems():
	# 	f.write(str(key) + ":" + str(value) + '\n')

		#initiate stemming
		# stemmer=stem.PorterStemmer()

		# for words in tokens:
		# 	allStemmed.append(stemmer.stem(words))
		# 	value = allStemmed

	