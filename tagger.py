# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 16:57:28 2019

@author: Pranav Krishna
"""
import nltk
taggedList=[]
with open(r"D:\bin\AIT-690\Assignments\Assignment-2\PA2\PA2\pos-train.txt") as file: # Use file to refer to the file object
   taggedSet = file.read()
   for line in taggedSet.split():
       tagTuples=nltk.tag.str2tuple(line)
       if(tagTuples[1] != None):
           taggedList.append(nltk.tag.str2tuple(line))
   
taggedDict={}
for x,y in taggedList:
    if(x in taggedDict.keys()):
        taggedDict[x].append(y)
    else:
        taggedDict[x]=[y]


tag='NNP'
previousTags=[]
for index,tup in enumerate(taggedList):
    if(tup[1] == tag):
        previousTags.append(taggedList[index-1][1])

word='Federal'
maxProb=0
for i in set(taggedDict[word]):
       WordTagprob=taggedDict[word].count(i)/len(taggedDict[word])
       if(prob>maxProb):
           tag=i
           maxProb=prob