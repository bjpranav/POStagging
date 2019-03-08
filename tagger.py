#Team GAP
import nltk
import sys
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
"""
train=sys.argv[1]
test=sys.argv[2]
key=sys.argv[3]
"""


with open(train) as trainset:  # Use file to refer to the file object
with open(r"C:\Users\alaga\Desktop\sem 2\AIT690\PA2\pos-train.txt") as trainset:


    tagged_trainset = trainset.read()
    # removing "[,],\n" which are not needed
    tagged_trainset=tagged_trainset.replace("[","")
    tagged_trainset=tagged_trainset.replace("]","")
    tagged_trainset = tagged_trainset.replace("\n", "")

    only_tags = []
    taggedList = []
    for line in tagged_trainset.split():

        tagTuples = nltk.tag.str2tuple(line)
        only_tags.append(tagTuples[1])
        if (tagTuples[1] != None):
            taggedList.append(nltk.tag.str2tuple(line))



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



with open(test) as testset:
with open(r"C:\Users\alaga\Desktop\sem 2\AIT690\PA2\pos-test.txt") as testset:

    untagged_testset = testset.read()
    # TEXT cleaning, removing "[,],\n"
    untagged_testset=untagged_testset.replace("[","")
    untagged_testset=untagged_testset.replace("]","")
    untagged_testset = untagged_testset.replace("\n", "")

""""
untagged_testset="No ,  it  was n't Black Monday . But while  the New York Stock Exchange did n't  fall apart  Friday as  the Dow Jones Industrial Average plunged  190.58 points -- most of  it in  the final hour "
"""


def extract_tags(tagged_text):

    only_tags = []
    for line in tagged_text:
        tagTuples = nltk.tag.str2tuple(line)
        if "|" in tagTuples[1].split():
            print(tagTuples[1])
        only_tags.append(tagTuples[1])
    return only_tags


def tagged_word(prev,curr):
    max_prob = []
    if curr in taggedDict:
        n = len(taggedDict[bigram[i]])
        unique = list(set(taggedDict[bigram[i]]))
        for u in unique:
            count_val = taggedDict[bigram[i]].count(u)
            prob1 = count_val / n

            mer = prev + ' ' + u
            if mer in double_tag_count.keys():
                prob2 = double_tag_count[mer] / single_tag_count[u]
                total_prob = prob1 * prob2
                max_prob.append(total_prob)
                type = unique[max_prob.index(max(max_prob))]

            elif bigram[i] in taggedDict:
                unique = list(set(taggedDict[bigram[i]]))
                max_val = taggedDict[bigram[i]].count(unique[0])
                type = unique[0]
                for u in unique:
                    n = taggedDict[bigram[i]].count(u)
                    if (n > max_val):
                        max_val = n
                        type = u

        prev = type
        return prev,type


#bigram
bigram=untagged_testset
tagged_test_string=[]
tagged=''
mer=''
bigram=bigram.split()
for i in range(0,len(bigram)):
    max_prob=[]

    if bigram[i] in taggedDict:

        if len(set(taggedDict[bigram[i]]))==1:
            type=taggedDict[bigram[i]][0]

        elif i==0:
            prev='.'
            curr=bigram[i]
            prev,type=tagged_word(prev,curr)


        else:
            curr = bigram[i]
            prev, type = tagged_word(prev, curr)
    else:
        type="NN"
        prev=type

    tagged=bigram[i]+'/'+type
    tagged_test_string.append(tagged)






"""
tagged_testset_key=r"No/RB ,/, [ it/PRP ][ was/VBD n't/RB Black/NNP Monday/NNP ]./. But/CC while/IN [ the/DT New/NNP York/NNP Stock/NNP Exchange/NNP ]did/VBD n't/RB [ fall/VB ]apart/RB [ Friday/NNP ]as/IN [ the/DT Dow/NNP Jones/NNP Industrial/NNP Average/NNP ]plunged/VBD [ 190.58/CD points/NNS ]--/: most/JJS of/IN [ it/PRP ]in/IN [ the/DT final/JJ hour/NN "
"""

with open(key) as testset_key:
with open(r"C:\Users\alaga\Desktop\sem 2\AIT690\PA2\pos-test-key.txt") as testset_key:

    tagged_testset_key = testset_key.read()
    ## TEXT cleaning, removing "[,],\n"
    tagged_testset_key = tagged_testset_key .replace("[", "")
    tagged_testset_key = tagged_testset_key .replace("]", "")
    tagged_testset_key= tagged_testset_key .replace("\n", "")


predicted=extract_tags(tagged_test_string)
actual=extract_tags(tagged_testset_key.split())

cnt=0
for i in range(0,len(predicted)):
    if predicted[i]==actual[i]:
        cnt+=1


accuracy=(cnt*100)/len(predicted)
print(accuracy)


confusion_matrix(actual,predicted)

cnf_matrix = confusion_matrix(actual,predicted)
