#! usr/bin/env python
import sys
# import time
from preProcesser import preProcessing
from documents import getDocs
import query as q
from merge import mergeBlocks

def indexGeneration(memorysize):
	#Fetch the docs and starts preProcessing by sending back text to lowercase
	docs = getDocs()

	#Tokenizing, normalizing and writing to blocks in prep for spimi
	preProcessing(docs,memorysize)

	#Merging blocks into one big index
	mergeBlocks()

def query():
	#instantiate a query class object such that it reads all the index once
	queryInput = q.Query()
	while True:
		inputed = raw_input("Enter your search query: ")
		#builds the query
		queryInput.makeQuery(inputed)

if __name__ == "__main__":
	indexGeneration(int(sys.argv[1]))
	query()