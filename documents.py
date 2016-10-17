import glob
from bs4 import BeautifulSoup

def getDocs():

	contentDict = dict()
	for filename in glob.glob('reuters21578/*.sgm'):
		with open(filename) as theFile:
			soup = BeautifulSoup(theFile.read(), 'html.parser')

			for texts in soup.findAll('reuters'):
				if texts.find('body'):
					contentDict[int(texts.get('newid'))] = texts.find('body').text.lower()
				if texts.find('text'):
					contentDict[int(texts.get('newid'))] = texts.find('text').text.lower()
	return contentDict

	# contentDict = dict()

	# for filename in glob.glob('reuters21578/*.sgm'):
	# 	with open(filename) as theFile:
	# 		parserId = ExtractId()

	# 		parserId.feed(theFile.read())

	# 		parserId.close()

	# 		parserText = ExtractText()

	# 		parserText.feed(theFile.read())

	# 		parserText.close()

	# 		print parserId.id

	# 		print parserText.body

	# 		for textId, text in parserId.id, parserText.body:
	# 			contentDict[textId] =  text

	# return contentDict


# import sgmllib

# class ExtractId(sgmllib.SGMLParser):
# 	def __init__(self, verbose=0):
# 		sgmllib.SGMLParser.__init__(self, verbose)
# 		self.id = []
# 		self.current_id = ''
# 		self.data = None

# 	def handle_data(self, data):
# 		if self.data is not None:
# 			self.data.append(data)


# 	def handle_starttag(self,tag, method, attrs):
# 		self.current_id = self.get_id_from_reuters(attrs)

# 	def handle_endtag(self, tag, method):
# 		self.id.append(self.current_id)

# 	def start_reuters(self, attrs):
# 		self.data = []

# 	def end_reuters(self):
# 		self.data = None

# 	def get_id_from_reuters(self, attrs):
# 		for key, val in attrs:
# 			if key == 'newid':
# 				return val

# class ExtractText(sgmllib.SGMLParser):
# 	def __init__(self, verbose=0):
# 		sgmllib.SGMLParser.__init__(self, verbose)
# 		self.body = []
# 		self.data = None

# 	def handle_data(self, data):
# 		if self.data is not None:
# 			self.data.append(data)

# 	def start_body(self, attrs):
# 		self.data = []

# 	def end_body(self):
# 		self.body.append(''.join(self.data))
# 		self.data = None


	

