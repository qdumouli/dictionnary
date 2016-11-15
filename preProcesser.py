import sys
import nltk
import re
from nltk import stem
try:
    import json
except ImportError:
    import simplejson as json 
from collections import OrderedDict
reload(sys)
sys.setdefaultencoding('utf-8')

# f = open("index/index.txt", "w")

def preProcessing(documents,memorysize):
	# tokenizer = word_tokenize.Word_Tokenize()

	postingsList = {}

	indexNumber = 00
	lengthNumber = 00

	numberOfTokensPerText = {}

	print "In preProcessing"

	#Stop words
	stopwords = ["Reuters", "reuters", "a", "about", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves"]

	#Number regex to remove numebrs
	numberRegex = re.compile('\d+')

	#Regex that removes non words and non numbers characters
	nonWordsRegex = re.compile('[^a-zA-Z0-9]+')
	

	#initiate empty array 
	allStemmed = []
	
	for key, value in documents.iteritems():
		tokens = []

		#Tokenize
		allWords = nltk.word_tokenize(value)

		#Checks for numbers and symbols in tokens and adds them to a set
		for words in allWords:
			#eliminate numbers
			if numberRegex.match(words):
				continue
			#eliminate symbols
			elif nonWordsRegex.match(words):
				continue
			#eliminate stop words
			elif words in stopwords:
				continue
			#if other then append to array of tokens
			else:
				tokens.append(words)



		#creates a set of all tokens
		# allWords = set(allWords)

		#Set operations to remove numbers, stop words and symbols
		# terms = allWords - numberRemover - stopwords - nonWordsRemover

		#gets the number of terms per docId
		numberOfTokensPerText[key] = len(allWords)

		#initiate stemming
		# stemmer=stem.PorterStemmer()

		# for words in tokens:
		# 	words = unicode(words, errors='ignore')
		# 	allStemmed.append(stemmer.stem(words))
		# 	value = allStemmed

		for term in tokens:
			term = unicode(term, errors="ignore")
			#The term is already in the postings list => check if the key is already in the postings list
			if term in postingsList:
				#getting the double array of postings List
				split = postingsList[str(term)]

				#initialize index to none for check later
				index = None
				#looping over all arrays in double array split and searching for key (index of doc)
				for i in range(len(split)):
					if key in split[i]:
						index = i

				#if a key already exist => get the number of occurences as of now, add 1 to it and then put this number back into the array
				if index is not None:
					splitAtIndex = split[index]
					occurencesOfTermInADoc = splitAtIndex[1] + 1
					postingsList[str(term)][index] = [key,occurencesOfTermInADoc]
				#otherwise just add the key and the occurence 1
				else:
					postingsList[str(term)].append([key,1])
			else:
				#if term not in postings list, initiate an empty array of document ids
				postingsList[str(term)] = [[key,1]]
				

		#if size of postingsList gets bigger than memorysize chosen, writes to a new block
		if ((sys.getsizeof(postingsList)) > memorysize):
			#sorting the term alphabetically
			sortedPostings = sorted(postingsList)
			sortedPostingsListTerms = OrderedDict()
			#sorting process for postingsList
			for item in sortedPostings:
				sortedPostingsListTerms[item] = postingsList[item]
			postingsList = sortedPostingsListTerms
			sortedPostingsListTerms = {}

			#for reading later, have to have this otherwise the postingsList are not sorted in the last index file
			if indexNumber < 100:
				formatedIndexNumber = '%03d' % indexNumber
			else:
				formatedIndexNumber = str(indexNumber)

			with open('index/index-' + formatedIndexNumber + '.json', 'w') as theFile:
				indexNumber+=1
				json.dump(postingsList, theFile)
			postingsList = {}

	print "Doing length"

	#writing to length file the docId : number of terms
	with open('length/length.json', 'w') as theFile:
		json.dump(numberOfTokensPerText, theFile)	






	print "Done with length"