import os, csv, random

os.chdir('C:\\Users\\jdyea\\OneDrive\\MoDyCo\\SWOP')
#%%
catLabels = [112,114,122,124,131,132,133,134,141,142,143,144,212,214,222,224,
			 231,232,233,234,241,242,243,244]
subNum = int(input("Subject number: "))

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
# Open stim file	
f = open(''.join(['ERP_stims\\stimList',str(listNum),'.txt']),'r')	
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
f = open(''.join(['stimTextFiles\\SUBJECT',str(subNum),'.txt']),'w')
f.close()
for block in range(1,3):
	f = open(''.join(['stimTextFiles\\stimBlock',str(block),'.txt']),'w')
	f.write('\t'.join(allItems[0]))
	f.write('\n')
	for sent in newStim[:240]:
		f.write('\t'.join(sent))
		f.write('\n')
	f.close()

# Save trial order for subject
f = open(''.join(['subjectStims\\ajtTrialOrderSub',str(subNum),'.txt']),'w')
for line in newStim:
	f.write('\t'.join(line))
	f.write('\n')
f.close()

# Save instructions
f = open('ERP_stims\\expInstr.txt','r')	
g = csv.reader(f,delimiter = '\t')
f2 = open(''.join(['ERP_stims\\expInstr',str(subNum),'.txt']),'w')
instr1 = ' '.join(["If it's good, press %s."%responses[1], str('\n'), "If it's bad, press %s."%responses[0],str('\n\n'),"Appuyez sur ESPACE pour continuer."])
for line in g:
	if line[3] == "%%%":
		line[3] = instr1
	f2.write('\t'.join(line))
	f2.write('\n')

f.close()
f2.close()