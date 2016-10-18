import json

class Query():
	#class initializer
	def __init__(self):
		with open("./index/index.json", 'r') as index:
			postingsList = json.load(index)
		#initialize attribute retrieveIndex. Useful in main such that object is created and readIndex only called once. Index static so that's ok
		self.retrieveIndex = postingsList

	def makeQuery(self,queryInput):
		#make query lowercase
		queryInput = queryInput.lower()

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

		#if the postingsList array is not null
		if postingsList:
			#intersect the set of postingsList
			results = list(set.intersection(*map(set, postingsList)))
		#if not, no results
		else:
			results = []

		print "Results: ", sorted(results)