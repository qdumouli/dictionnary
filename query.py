import processIndex

class Query:
	# def __init__(self):

	# 	self.retrieveIndex = processIndex.readIndex()

	def makeQuery(self, queryInput):
		retrieveIndex = processIndex.readIndex();
		queryInput = queryInput.lower()
		terms = queryInput

		listOfPostingsList = []

		if terms in retrieveIndex:
			listOfPostingsList.append(retrieveIndex[terms])
		print "Results: ", listOfPostingsList[0]