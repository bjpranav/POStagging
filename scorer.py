
import sys
import nltk

#accuracy test

predicted=sys.argv[1]
key=sys.argv[2]


def extract_tags(tagged_text):
    only_tags = []
    for line in tagged_text:
        tagTuples = nltk.tag.str2tuple(line)
        if "|" in list(tagTuples[1]):
            tagTuples=(tagTuples[0],tagTuples[1].split('|')[0])
        only_tags.append(tagTuples[1])
    return only_tags


predicted=open(predicted)
predicted=predicted.read()

tagged_testset_key= open(key)
tagged_testset_key=tagged_testset_key.read()
tagged_testset_key = tagged_testset_key .replace("[", "")
tagged_testset_key = tagged_testset_key .replace("]", "")
tagged_testset_key= tagged_testset_key .replace("\n", "")

#testset = open(r"C:\Users\alaga\Desktop\sem 2\AIT690\POStagging\pos-test-key.txt")



predicted=extract_tags(predicted.split())
actual=extract_tags(tagged_testset_key.split())


cnt=0
for i in range(0,len(predicted)):
    if predicted[i]==actual[i]:
        cnt+=1


accuracy=(cnt*100)/len(predicted)

print(accuracy)