import csv, random

#import os
#os.chdir('C:\\Users\\jdyea\\OneDrive\\MoDyCo\\SWOP')
#os.chdir('C:\\Users\\AdminS2CH\\Desktop\\Experiments\\eprime')
#%%
catLabels = [112,114,122,124,131,132,133,134,141,142,143,144,212,214,222,224,
			 231,232,233,234,241,242,243,244]
subNum = int(input("Subject number: "))

nLists = 10 # Number of blocks for stimulus presentation
maxRep = 3 # Maximum number of the same response allowed in a row

# Assign list number to even/odd subjects
listNum = 2 # Default
if subNum % 2 == 1: # Change if participant number is odd
	listNum = 1
# Assign response category to alternate every 2 participants
responses = ['j','f'] # Default
if subNum % 4 < 2: # Change for 2 out of every 4 subjects
	responses = ['f','j']
# Open practice stim file
f = open('SWOPstims\\practice.txt','r')
g = csv.reader(f,delimiter = '\t')
h = open('SWOPstims\\stimTextFiles\\practiceBlock.txt','w')
for line in g:
    if line[4] == '1': # Condition column: 1 = Violation, 2 = Canonical
        line[-1] = responses[1]
    elif line[4] == '2':
        line[-1] = responses[0]
    txtLine = '\t'.join(line)
    h.write(txtLine)
    h.write('\n')	

f.close()
h.close() # Save practice stim file
# Open master stim file	
#f = open(''.join(['ERP_stims\\stimList',str(listNum),'.txt']),'r')
f = open(''.join(['SWOPstims\\stimList',str(listNum),'.txt']),'r')	
g = csv.reader(f,delimiter = '\t')
# Assign correct reponses to items
allItems = []
for line in g:
	if line[5] == '1': # Condition column: 1 = Violation, 2 = Canonical
		line[-1] = responses[1]
	elif line[5] == '2':
		line[-1] = responses[0]
	allItems.append(line)

def checkRepeats(block,inarow):
	for i, sent in enumerate(block):
		if i == 0:
			pass
		elif sent[5] == block[i-1][5]:
			inarow += 1
		else:
			inarow = 1
		if inarow > maxRep:
			break
	return inarow
	
# Shuffle
random.shuffle(allItems) # Shuffle all the sentences
newStim = []
rpt,carryOver = maxRep + 1, 1
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
		for j in toPop: # Remove items that have been put in block
			allItems.pop(j)
	while rpt > maxRep:
		random.shuffle(currBlock)
		if block > 0 and newStim[-1][5] == currBlock[0][5]:
			rpt = checkRepeats(currBlock, carryOver + 1)
		else:
			rpt = checkRepeats(currBlock, 1)
	for sent in currBlock:
		newStim.append(sent) # Add sentences to stimulus list
	carryOver = rpt
	rpt = maxRep + 1
f.close()

totItems = len(newStim)
iPerList = int(totItems / nLists)

for listNum in range(1, nLists + 1):
	f = open(''.join(['SWOPstims\\stimTextFiles\\stimBlock',str(listNum),'.txt']),'w')
	f.write(''.join(['\t'.join(allItems[0]),'\n'])) # Write header
	start = (listNum-1)*(iPerList)
	for sent in newStim[start : start + iPerList]:
		f.write(''.join(['\t'.join(sent),'\n']))
	f.close()

# Save trial order for subject
f = open(''.join(['SWOPstims\\subjectStims\\ajtTrialOrderSub',str(subNum),'.txt']),'w')
for line in newStim:
	f.write(''.join(['\t'.join(line),'\n']))
f.close()

# Save instructions
f1 = open('SWOPstims\\expInstr%s.txt'%responses[0],'r')
g = csv.reader(f1,delimiter = '\t')
f2 = open(''.join(['SWOPstims\\stimTextFiles\\expInstr',str(subNum),'.txt']),'w')

for line in g: # Copy instructions into subject-specific file
	f2.write(''.join(['\t'.join(line),'\n']))
f1.close()
f2.close()