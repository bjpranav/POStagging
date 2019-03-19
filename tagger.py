import nltk
import sys
from nltk.stem.wordnet import WordNetLemmatizer
import time



#train=sys.argv[1]
#test=sys.argv[2]

start = time.time()
#trainset = open(train)
trainset = open(r"D:\bin\AIT-690\Assignments\Assignment-2\pos-train.txt")
tagged_trainset = trainset.read()

# removing "[,],\n" which are not needed
tagged_trainset = tagged_trainset.replace("[", "")
tagged_trainset = tagged_trainset.replace("]", "")
tagged_trainset = tagged_trainset.replace("\n", "")

only_tags = []
taggedList = []
for line in tagged_trainset.split():
    tagTuples = nltk.tag.str2tuple(line)
    if (tagTuples[1] != None):
        if ("|" in list(tagTuples[1])):
            tagTuples = (tagTuples[0], tagTuples[1].split('|')[0])
        taggedList.append(tagTuples)
        only_tags.append(tagTuples[1])

taggedDict={}
for x,y in taggedList:
    if(x in taggedDict.keys()):
        taggedDict[x].append(y)
    else:
        taggedDict[x]=[y]


double_tag_count={}
single_tag_count = {}
for i in range(0,len(only_tags)):
    flag_single = 0
    if (only_tags[i] in single_tag_count.keys() and flag_single == 0):
        single_tag_count[only_tags[i]] = single_tag_count[only_tags[i]] + 1
        flag_single = 1
    elif(flag_single == 0):
        single_tag_count[only_tags[i]] = 1
    if(i<len(only_tags)-1):
        mer = only_tags[i] + ' ' + only_tags[i + 1]
        if mer in double_tag_count.keys():
            double_tag_count[mer] = double_tag_count[mer] + 1
        else:
            double_tag_count[mer] = 1


#testset = open(test)
testset=open(r"D:\bin\AIT-690\Assignments\Assignment-2\\pos-test.txt")
untagged_testset = testset.read()

# TEXT cleaning, removing "[,],\n"
untagged_testset = untagged_testset.replace("[", "")
untagged_testset = untagged_testset.replace("]", "")
untagged_testset = untagged_testset.replace("\n", "")


def tagged_word(prev,curr):
    max_prob = []
    if curr in taggedDict:
        n = len(taggedDict[bigram[i]])
        unique = list(set(taggedDict[bigram[i]]))
        for u in unique:
            count_val = taggedDict[bigram[i]].count(u)
            prob1 = count_val / single_tag_count[u]
            mer = prev + ' ' + u
            if mer in double_tag_count.keys():
                prob2 = double_tag_count[mer] / single_tag_count[u]
                total_prob = prob1 * prob2
                max_prob.append(total_prob)
                typeVal = unique[max_prob.index(max(max_prob))]

            elif bigram[i] in taggedDict:
                unique = list(set(taggedDict[bigram[i]]))
                max_val = taggedDict[bigram[i]].count(unique[0])
                typeVal = unique[0]
                for u in unique:
                    n = taggedDict[bigram[i]].count(u)
                    if (n > max_val):
                        max_val = n
                        typeVal = u
            

        prev = typeVal
        return prev,typeVal



bigram=untagged_testset
tagged_test_string=[]
tagged=''
mer=''
bigram=bigram.split()
for i in range(0,len(bigram)):
    max_prob=[]

    if bigram[i] in taggedDict:

        if len(set(taggedDict[bigram[i]]))==1:
            typeVal=taggedDict[bigram[i]][0]

        elif i==0:
            prev='.'
            curr=bigram[i]
            prev,typeVal=tagged_word(prev,curr)


        else:
            curr = bigram[i]
            prev, typeVal = tagged_word(prev, curr)
    else:
        if bigram[i][0].isdigit()==True:
            typeVal = "CD"
        elif bigram[i][-1]=='s':
            typeVal = "NNS"
        elif bigram[i][-2:]=='ed':
            typeVal = "VBN"
        elif bigram[i][-4:] == 'able':
            typeVal = "JJ"
        elif bigram[i][0].isupper()==True:
            typeVal = "NNP"
        elif bigram[i][-3:] == 'ing':
            typeVal = "VBG"
        else:
            typeVal = "NN"
        prev=typeVal

    tagged=bigram[i]+'/'+typeVal
    tagged_test_string.append(tagged)

'''
for i in range(0,(len(tagged_test_string)-2)):
    currTag=nltk.tag.str2tuple(tagged_test_string[i])[1]
    nextTag=nltk.tag.str2tuple(tagged_test_string[i+1])[1]
    if(i>0):
        prevTag=nltk.tag.str2tuple(tagged_test_string[i-1])[1]
    currWord=nltk.tag.str2tuple(tagged_test_string[i])[0]
'''

for i in range(0,(len(tagged_test_string)-2)):
    currTag=nltk.tag.str2tuple(tagged_test_string[i])[1]
    nextTag=nltk.tag.str2tuple(tagged_test_string[i+1])[1]
    if(i>0):
        prevTag=nltk.tag.str2tuple(tagged_test_string[i-1])[1]
    currWord=nltk.tag.str2tuple(tagged_test_string[i])[0]
    
    if(currWord == 'a' and prevTag not in [',','.',':']):
        typeVal='DT'
        tagged=bigram[i]+'/'+typeVal
        tagged_test_string[i]=tagged

    elif(currTag == 'RP' and prevTag not in ["VB","VBD","VBG","VBN","VBZ","VBP"]):
        typeVal='IN'
        tagged=bigram[i]+'/'+typeVal
        tagged_test_string[i]=tagged
        
    elif(currTag == 'RP' and prevTag not in ["VB","VBD","VBG","VBN","VBZ","VBP"]):
        typeVal='IN'
        tagged=bigram[i]+'/'+typeVal
        tagged_test_string[i]=tagged
        
    elif(currTag == 'VB' and prevTag == "DT"):
        typeVal='NN'
        tagged=bigram[i]+'/'+typeVal
        tagged_test_string[i]=tagged
    elif(currTag == 'WDT' and prevTag not in ["NN","NNS",',']):
        typeVal='IN'
        tagged=bigram[i]+'/'+typeVal
        tagged_test_string[i]=tagged
 

with open('pos-test-with-tags.txt', 'w') as f:
    for item in tagged_test_string:
        f.write("%s\n" % item)

end = time.time()
runtime = end-start
print("Run Time: ",runtime)
print("pos-test-with-tags.txt")
