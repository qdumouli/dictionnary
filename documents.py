import glob
# from bs4 import BeautifulSoup
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
			#initialize body is open
			bodyOpen = False
			#initialize text is open for cases where there is no body only a text
			textOpen = False
			#parses the sgm files
			# soup = BeautifulSoup(theFile.read(), 'html.parser')
			for line in theFile:
				#if body is open
				if bodyOpen:
					#find the end of the file </BODY> tag
					endOfLineDoc = line.find(BodyEnd)
					#if this is the end of the file
					if endOfLineDoc != -1:
						#add the rest of the words to the body
						body += line[:endOfLineDoc]
						#add body to the dictionnary containing docId: body
						contentDict[newId] = body
						#set body back to nothing
						body = ""
						#set body to false to fetch next <REUTERS tag
						bodyOpen = False
						#reset newId
						newId = -1
					#if not end of file
					else:
						#append line to the body and continue
						body += line
				#same as body but if there is no <BODY> tag for a <REUTERS tag, this will take care of it
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

				# this part executes when we are fetching for a new <REUTERS tag
				else:
					#find a <REUTERS opening tag
					startingLine = line.find(ReutersStart)
					#if it's here
					if startingLine != -1:
						# print int(re.search("NEWID=\"(\d*)", line).group(1))
						#get the newId. regex search on NEWID tag with (\d* => number with multiple 1-9 numbers) 
						newId = int(re.search("NEWID=\"(\d*)", line).group(1))
					#search for text start or body start
					textStart = line.find(TextStart)
					bodyStart = line.find(BodyStart)
					#if body Start was found
					if bodyStart != -1:
						#initialize body open to True to perform line reading 
						bodyOpen = True
						#get the starting line of the doc
						startingLineOfDoc = line[bodyStart+len(BodyStart):]
						#get the end of line of the doc
						endOfLineDoc = startingLineOfDoc.find(BodyEnd)
						#if the text ends
						if endOfLineDoc != -1:
							#append to the body the start of the line to the end :endOfLineDoc
							body = startingLineOfDoc[:endOfLineDoc]
							#Set body to false to getch new Reuters tag
							bodyOpen = False
							#set body to empty for next search
							body = ""
						#if the end of the text is not right away
						else:
						#append the line to the body
							body += startingLineOfDoc
					#same logic as for bodyStart != -1 but with Text if there is no body present in the reuters tag
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
	#gives back the dictionary
	return contentDict
	

