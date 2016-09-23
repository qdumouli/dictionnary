import glob
import time
from tokenizer import preProcessing

docArray = list()

start = time.time()
for filename in glob.glob('reuters21578/reut2-000.sgm'):
	preProcessing(filename)

end = time.time()
print(end - start)

# soup = BeautifulSoup(data)

# for content in soup.findAll('reuters'): 
# 	if(content.find('body')):
# 		tuple = content['newid'], content.find('body').contents[0]
# 	else:
# 		tuple = content['newid'], content.find('text').contents[0]

	

# 	docArray.append(tuple)



#