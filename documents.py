import glob
import sys
from bs4 import BeautifulSoup
print sys.path
import re

ReutersStart = "<REUTERS"
TextStart = "<TEXT>"
TextEnd = "</TEXT>"
BodyStart = "<BODY>"
BodyEnd = "</BODY>"

def getDocs():

	#Creates empty dictionnary
	contentDict = dict()
	#goes through all files in folder
	for filename in glob.glob('reuters21578/*.sgm'):
		with open(filename) as theFile:
			body = ''
			bodyOpen = False
			textOpen = False
			#parses the sgm files
			# soup = BeautifulSoup(theFile.read(), 'html.parser')
			for line in TheFile:
				if bodyOpen:
					endOfLineDoc = line.find(BodyEnd)
					if endOfLineDoc != -1:
						body += line[:endOfLineDoc]
						contentDict[newId] = body
						body = ""
						bodyOpen = False
						newId = -1
					else:
						body += line
				elif textOpen:
					endOfLineDoc = line.find(TextEnd)
					if endOfLineDoc != -1:
						body += line[:endOfLineDoc]
						contentDict[newId] = body
						body = ""
						textOpen = False
						newId = -1
					else:
						body += line

				else:
					startingLine = line.find(ReutersStart)
					if startingLine != -1:
						newId = int(re.search("NEWID\"(\d+)", line).group(1))
					textStart = line.find(TextStart)
					bodyStart = line.find(BodyStart)
					if bodyStart != -1:
						bodyOpen = True
						startingLineOfDoc = line[bodyStart+len(BodyStart):]
						endOfLineDoc = startingLineOfDoc.find(BodyEnd)
						if endOfLineDoc != -1:
							body = startingLineOfDoc[:endOfLineDoc]
							bodyOpen = False
							body = ""
						else:
							body += startingLineOfDoc
					elif textStart != -1:
						textOpen = True
						startingLineOfDoc = line[textStart+len(TextStart):]
						endOfLineDoc = startingLineOfDoc.find(TextEnd)
						if endOfLineDoc != -1:
							body = startingLineOfDoc[:endOfLineDoc]
							textOpen = False
							body = ""
						else:
							body += startingLineOfDoc


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
	

