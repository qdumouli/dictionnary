import processIndex

def makeQuery(queryInput):
	retrieveIndex = processIndex.readIndex()
	queryInput = queryInput.lower()
	queryTerms = queryInput

	split = queryTerms.split(" ")


	listOfPostingsList = []

	# if terms in self.retrieveIndex:
	# 	listOfPostingsList.append(self.retrieveIndex[terms])
	# print "Results: ", listOfPostingsList[0]

	termCounter = 0
	for queryTerm in split:
		termCounter+=1
		if queryTerm in retrieveIndex:
			listOfPostingsList.append(retrieveIndex[queryTerm])

	if listOfPostingsList:
		results = list(set.intersection(*map(set, listOfPostingsList)))
	else:
		print "Yo"
		# results = [filter(lambda x: x in listOfPostingsList, sublist) for sublist in listOfPostingsList]

	print "Number of terms", termCounter
	print "Results: ", sorted(results)