import json
from math import log
from BM25 import calculateAverageLength, getLength
from collections import Counter

class Query():
	#class initializer
	def __init__(self):
		with open("./index/index.json", 'r') as index:
			postingsList = json.load(index)
		#initialize attribute retrieveIndex. Useful in main such that object is created and readIndex only called once. Index static so that's ok
		self.retrieveIndex = postingsList
		with open('./length/length.json', 'r') as length:
			numberOfTokensPerText = json.load(length)
		#initialize attribute numOfTokens. Useful in main such that object is created and the json file with all docs and their length loads only once.
		self.numOfTokens = numberOfTokensPerText

	def makeQuery(self,queryInput):
		#make query lowercase
		queryInput = queryInput
		#k1 value
		k1 = 1.2
		#b value
		b = 0.75

		#split the query if there is a space => we will take this as an AND query
		split = queryInput.split(" ")

		#initialize postingsList array
		postingsList = []

		#for each term in the queried search
		for queryTerm in split:
			#if the term is in the index
			if queryTerm in self.retrieveIndex:
				#add its postingsList to the array
				postingsList.append(self.retrieveIndex[queryTerm])
			#if not in the index then add an empty array for intersection
			else:
				postingsList.append([])

		# #if the postingsList array is not null
		if postingsList:
			#initialize epty list of documents ids
			listOfDocIds = []
			#split it into the different postings list of terms [[[],[]],[[],[]]] => [[],[]] and [[],[]]
			for results in postingsList:
				#split again each postings list that contains query term [[], []] => [],[]
				for result in results:
					#adding the docId of the result sets to a new array
					listOfDocIds.append(result[0])
			#if an element in the array has a counter that is more than 1 => return the list in result
			results = [item for item, count in Counter(listOfDocIds).items() if count > 1]
		#if not, no results
		else:
			results = []

		#empty dictionnary to store the doc id and the score of each query
		totalScore = {}

		# if results exist
		if results:
			# for each query term
			for queryTerm in split:
				#if the query term is in the index (it is since it was in result)
				if queryTerm in self.retrieveIndex:
					#for each documentid and frequency of term queryTerm in our index
					for documentId, frequency in self.retrieveIndex[queryTerm]:
						#if the doc id is in the results => start calculating BM25
						if documentId in results:
							#the log input, total number of docs over the number of documents the term appears in
							logInput = log(21578 / (len(self.retrieveIndex[queryTerm])))
							#the second part of the equation, getLength gets the number of terms in a certain doc id
							#calculateAverageLength gets the average number of terms for all docs => for better performace, could put it outside the calculation
							secondPart = ((frequency * (k1 + 1))/(frequency + k1*(1-b+b*(getLength(self.numOfTokens, documentId)/(calculateAverageLength(self.numOfTokens))))))
							#the final result for a query term dependant of the first doc it was found in
							total = logInput * secondPart

							# if the calculation already exists for a doc id, then per the formula, sum all of them up
							if documentId in totalScore:
								#summing part
								totalScore[documentId] += total
							#if the calculation is not in the totalScore dictionnary yet, initialize its value
							else:
								#first total
								totalScore[documentId] = total

		#sorting the dictionnary in descending order of the values
		totalScore = sorted(totalScore.items(), key=lambda x:x[1], reverse=True)

		#initialize our counter to print the top 10
		i = 0
		# fetch all keys and values in dictionnary totalScore
		for key, values in totalScore:
			#increment i 
			i+=1
			# if i is less than 10 then print the next highest score
			if i <= 10:
				print str(key) + " scores " + str(values)
			#top ten was already established
			else:
				#go on with your day number!
				continue