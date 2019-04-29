import os, csv, random

#os.chdir('C:\\Users\\jdyea\\OneDrive\\MoDyCo\\SWOP')
os.chdir('C:\\Users\\AdminS2CH\\Desktop\\Experiments\\eprime')
#%%
catLabels = [112,114,122,124,131,132,133,134,141,142,143,144,212,214,222,224,
			 231,232,233,234,241,242,243,244]
subNum = int(input("Subject number: "))

nLists = 10

# Assign list number to even/odd subjects
if subNum % 2 == 1:
	listNum = 1
else:
	listNum = 2
# Assign response category to alternate every 2 participants
if subNum % 4 < 2: 
	responses = ['f','j']
else:
	responses = ['j','f']
# Open practice stim file
f = open('SWOPstims\\practice.txt','r')
g = csv.reader(f,delimiter = '\t')
h = open('SWOPstims\\stimTextFiles\\practiceBlock.txt','w')
for line in g:
    if line[4] == '1': # Condition column: 1 = Violation, 2 = Canonical
        line[-1] = responses[0]
    elif line[4] == '2':
        line[-1] = responses[1]
    txtLine = '\t'.join(line)
    h.write(txtLine)
    h.write('\n')	

f.close()
h.close()
# Open stim file	
#f = open(''.join(['ERP_stims\\stimList',str(listNum),'.txt']),'r')
f = open(''.join(['SWOPstims\\stimList',str(listNum),'.txt']),'r')	
g = csv.reader(f,delimiter = '\t')
# Assign correct reponses to items
allItems = []
for line in g:
	if line[5] == '1': # Condition column: 1 = Violation, 2 = Canonical
		line[-1] = responses[0]
	elif line[5] == '2':
		line[-1] = responses[1]
	allItems.append(line)
	
# Shuffle
random.shuffle(allItems) # Shuffle all the sentences
newStim = []
for block in range(20): # 24 categories x 20 blocks = 480 items
	currBlock = []
	# For each block, find the first sentence with the desired category and append to block
	for cat in catLabels:
		toPop = []
		for i in range(len(allItems)):
			if allItems[i][6] == str(cat):
				toPop.append(i)
				currBlock.append(allItems[i])
				break
		toPop.sort(reverse = True)
		for j in toPop: # Remove items that have been put in blocks
			allItems.pop(j)
	random.shuffle(currBlock)
	while block > 0 and newStim[-1][6] == currBlock[0][6]:
		random.shuffle(currBlock)
	for sent in currBlock:
		newStim.append(sent) # Add sentences to stimulus list
# Save text files and subject flag		
f.close()
# f = open(''.join(['SWOPstims\\stimTextFiles\\SUBJECT',str(subNum),'.txt']),'w')
# f.close()

totItems = len(newStim)
iPerList = int(totItems / nLists)

for listNum in range(1, nLists + 1):
	f = open(''.join(['SWOPstims\\stimTextFiles\\stimBlock',str(listNum),'.txt']),'w')
	f.write('\t'.join(allItems[0]))
	f.write('\n')
	start = (listNum-1)*(iPerList)
	for sent in newStim[start : start + iPerList]:
		f.write('\t'.join(sent))
		f.write('\n')
	f.close()

# Save trial order for subject
f = open(''.join(['SWOPstims\\subjectStims\\ajtTrialOrderSub',str(subNum),'.txt']),'w')
for line in newStim:
	f.write('\t'.join(line))
	f.write('\n')
f.close()

# Save instructions
if responses[0] == 'f':
    f = open('SWOPstims\\expInstrJ.txt','r')	
else:
    f = open('SWOPstims\\expInstrF.txt','r')
g = csv.reader(f,delimiter = '\t')
f2 = open(''.join(['SWOPstims\\stimTextFiles\\expInstr',str(subNum),'.txt']),'w')

for line in g:
	f2.write('\t'.join(line))
	f2.write('\n')
f.close()
f2.close()