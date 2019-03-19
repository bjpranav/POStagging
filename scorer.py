# -*- coding: utf-8 -*-



import sys
import nltk
import numpy as np
import pandas as pd


#accuracy test


'''
predicted=sys.argv[1]
key=sys.argv[2]
'''

def extract_tags(tagged_text):
    only_tags = []
    for line in tagged_text:
        tagTuples = nltk.tag.str2tuple(line)
        if "|" in list(tagTuples[1]):
            tagTuples=(tagTuples[0],tagTuples[1].split('|')[0])
        only_tags.append(tagTuples[1])
    return only_tags


#predicted=open(predicted)
predicted = open(r"C:\Users\alaga\Desktop\sem 2\AIT690\POStagging\pos-test-with-tags.txt")
predicted=predicted.read()

#tagged_testset_key= open(key)
tagged_testset_key = open(r"C:\Users\alaga\Desktop\sem 2\AIT690\POStagging\pos-test-key.txt")
tagged_testset_key=tagged_testset_key.read()

tagged_testset_key = tagged_testset_key .replace("[", "")
tagged_testset_key = tagged_testset_key .replace("]", "")
tagged_testset_key= tagged_testset_key .replace("\n", "")




predicted=extract_tags(predicted.split())
actual=extract_tags(tagged_testset_key.split())

tags=set(actual)

A = np.zeros((len(tags), len(tags)))
confusion_matrix = pd.DataFrame(A, index=tags, columns=tags)


cnt=0
for i in range(0,len(predicted)):
    if predicted[i]==actual[i]:
        cnt+=1
    confusion_matrix.at[predicted[i], actual[i]]=confusion_matrix.at[predicted[i], actual[i]] + 1

accuracy=(cnt*100)/len(predicted)

with open('pos-tagging-report.txt', 'w') as f:
#np.savetxt(r'pos-tagging-report.txt', confusion_matrix, fmt='%d',delimiter = "   ")
    f.write("Accuracy: %s" % accuracy+"\n")
    confusion_matrix.to_csv('pos-tagging-report.txt', header=True, index=True, sep='\t', mode='a')
    
print("pos-tagging-report.txt")

