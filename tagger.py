#Team GAP
import nltk
import sys
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from nltk.stem.wordnet import WordNetLemmatizer






"""
train=sys.argv[1]
test=sys.argv[2]
key=sys.argv[3]
"""



#trainset = open(train)
trainset = open(r"C:\Users\alaga\Desktop\sem 2\AIT690\POStagging\pos-train.txt")

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


single_tag_count = {}
for x,y in taggedList:
    if(y in single_tag_count.keys()):
        single_tag_count[y]=single_tag_count[y]+1
    else:
        single_tag_count[y]=1


double_tag_count={}
mer=''
for i in range(0,len(only_tags)-1):
    mer=only_tags[i]+' '+only_tags[i+1]
    if mer in double_tag_count.keys():
        double_tag_count[mer]=double_tag_count[mer]+1
    else:
        double_tag_count[mer]=1



#testset = open(test)
testset=open(r"C:\Users\alaga\Desktop\sem 2\AIT690\POStagging\pos-test.txt")

untagged_testset = testset.read()
# TEXT cleaning, removing "[,],\n"
untagged_testset = untagged_testset.replace("[", "")
untagged_testset = untagged_testset.replace("]", "")
untagged_testset = untagged_testset.replace("\n", "")


""""
untagged_testset="No ,  it  was n't Black Monday . But while  the New York Stock Exchange did n't  fall apart  Friday as  the Dow Jones Industrial Average plunged  190.58 points -- most of  it in  the final hour "
"""


def extract_tags(tagged_text):
    only_tags = []
    for line in tagged_text:
        tagTuples = nltk.tag.str2tuple(line)
        if "|" in list(tagTuples[1]):
            tagTuples=(tagTuples[0],tagTuples[1].split('|')[0])
        only_tags.append(tagTuples[1])
    return only_tags


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


COUNT=0
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
            COUNT=COUNT+1

        elif i==0:
            prev='.'
            curr=bigram[i]
            prev,typeVal=tagged_word(prev,curr)


        else:
            curr = bigram[i]
            prev, typeVal = tagged_word(prev, curr)
    else:
        typeVal="NN"
        prev=typeVal

    tagged=bigram[i]+'/'+typeVal
    tagged_test_string.append(tagged)

firstTag=tagged_test_string[0]
prev = nltk.tag.str2tuple(firstTag)[1]
Lem = WordNetLemmatizer()

#nltk.download('wordnet')

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
        #print(tagged_test_string[i])
    elif(currWord.istitle() and currTag == 'NN' and prevTag != '.'):
        typeVal='NNP'
        tagged=bigram[i]+'/'+typeVal
        tagged_test_string[i]=tagged
    elif(currWord.endswith('s') and Lem.lemmatize(currWord)==currWord[:-1] and currTag == 'NN'):
        typeVal='NNS'
        tagged=bigram[i]+'/'+typeVal
    elif(currTag == 'RP' and prevTag not in ["VB","VBD","VBG","VBN","VBZ","VBP"]):
        typeVal='IN'
        tagged=bigram[i]+'/'+typeVal
        tagged_test_string[i]=tagged
    elif(currTag == 'NN' and currWord.replace('.','',1).isdigit()):
        typeVal='CD'
        tagged=bigram[i]+'/'+typeVal
        tagged_test_string[i]=tagged




with open('pos-test-with-tags.txt', 'w') as f:
    for item in tagged_test_string:
        f.write("%s\n" % item)




