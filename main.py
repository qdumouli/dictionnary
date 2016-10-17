#! usr/bin/env python
import sys
import time
from preProcesser import preProcessing
from documents import getDocs
from query import makeQuery
import processIndex

def indexGeneration(memorysize):
	print "Fetching the docs"
	docs = getDocs()
	print "Number of docs ", len(docs)

	preProcessing(docs,memorysize)

	# queryInput = Query(postingsList)
	# while True:
	# 	inputed = raw_input("Enter your search query: ")
	# 	result = queryInput.makeQuery(inputed)
	while True:
		inputed = raw_input("Enter your search query: ")
		makeQuery(inputed)

if __name__ == "__main__":
	indexGeneration(int(sys.argv[1]))