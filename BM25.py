import json
import sys
#setting encoding for json processing
reload(sys)
sys.setdefaultencoding('utf-8')

#gets the average number of terms per docs over whole corpus
def calculateAverageLength(numberOfTokensPerText):
	totalNumber = 0
	for key, value in numberOfTokensPerText.iteritems():
		totalNumber += int(value)
	return int(totalNumber/21578)
#gets the number of term in a single doc, docId passed as parameters
def getLength(numberOfTokensPerText, docId):
	#make sure docId is in unicode for eval with json value
	docId = unicode(docId)
	for key, value in numberOfTokensPerText.iteritems():
		if key == docId:
			return int(value)

