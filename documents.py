import glob
import sys
from bs4 import BeautifulSoup
print sys.path

def getDocs():

	#Creates empty dictionnary
	contentDict = dict()
	#goes through all files in folder
	for filename in glob.glob('reuters21578/*.sgm'):
		with open(filename) as theFile:
			#parses the sgm files
			soup = BeautifulSoup(theFile.read(), 'html.parser')

			#if tag reuters found
			for texts in soup.findAll('reuters'):
				#if tag body found
				if texts.find('body'):
					#dictionary key is the id while whole body is the value
					contentDict[int(texts.get('newid'))] = texts.find('body').text
					# contentDict[int(texts.get('newid'))] = texts.find('body').text.lower()
				#if no body tag found but there is a text tag
				if texts.find('text'):
					#dictionary key is the id while whole text is the value
					contentDict[int(texts.get('newid'))] = texts.find('text').text
					# contentDict[int(texts.get('newid'))] = texts.find('text').text.lower()
	#gives back the dictionary
	return contentDict
	

