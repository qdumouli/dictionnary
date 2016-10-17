#! usr/bin/env python

import time
from preProcesser import preProcessing
from documents import getDocs
from query import Query
import processIndex

def indexGeneration():
	print "Fetching the docs"
	docs = getDocs()
	print "Number of docs ", len(docs)

	preProcessing(docs)

	# queryInput = Query(postingsList)
	# while True:
	# 	inputed = raw_input("Enter your search query: ")
	# 	result = queryInput.makeQuery(inputed)


def query():
	queryInput = Query()
	while True:
		inputed = raw_input("Enter your search query: ")
		queryInput.makeQuery(inputed)



if __name__ == "__main__":
	indexGeneration()
	query()