import csv, random

#import os
#os.chdir('C:\\Users\\jdyea\\OneDrive\\MoDyCo\\SWOP')
#os.chdir('C:\\Users\\AdminS2CH\\Desktop\\Experiments\\eprime')
#%%
catLabels = [112,114,122,124,131,132,133,134,141,142,143,144,212,214,222,224,
			 231,232,233,234,241,242,243,244]
#subNum = int(input("Subject number: "))
subNum = 999

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
		if inarow > 3:
			break
	return inarow
	
# Shuffle
random.shuffle(allItems) # Shuffle all the sentences
newStim = []
rpt,carryOver = 4, 1
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
	while rpt > 3:
		random.shuffle(currBlock)
		if block > 0 and newStim[-1][5] == currBlock[0][5]:
			rpt = checkRepeats(currBlock,carryOver + 1)
		else:
			rpt = checkRepeats(currBlock,1)
	for sent in currBlock:
		newStim.append(sent) # Add sentences to stimulus list
	carryOver = rpt
	rpt = 4
f.close()

totItems = len(newStim)
iPerList = int(totItems / nLists)

for listNum in range(1, nLists + 1):
	f = open(''.join(['SWOPstims\\stimTextFiles\\stimBlock',str(listNum),'.txt']),'w')
	f.write('\t'.join(allItems[0]))
	f.write('\n')
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
f = open('SWOPstims\\expInstr%s.txt'%responses[0],'r')
g = csv.reader(f,delimiter = '\t')
f2 = open(''.join(['SWOPstims\\stimTextFiles\\expInstr',str(subNum),'.txt']),'w')

for line in g:
	f2.write('\t'.join(line))
	f2.write('\n')
f.close()
f2.close()