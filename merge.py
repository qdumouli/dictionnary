import json
import glob

def mergeBlocks():
	#open output file
	print "In mergeBlocks"
	with open('./index/index.json', 'a+') as theFile:
		#initialize empty dict
		dictionary = {}
		#iterates through all blocks
		for filename in glob.glob('index/index-*.json'):
			with open(filename, 'r') as blocks:
				#loads term-postingsList from blocks
				postingsList = json.load(blocks)
				#iterates through keys
				for key, value in postingsList.iteritems():
					#if term is in dict add postingsList
					if key in dictionary:
						dictionary[key].extend(value)
					else:
						#initialize term with first postingsList
						dictionary[key] = value
		#writes to json
		json.dump(dictionary, theFile)

