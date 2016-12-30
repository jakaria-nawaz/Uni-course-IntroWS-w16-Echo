import pandas as pd
import numpy as np
import time
import math
import re

store = pd.HDFStore('store.h5')
df1 = store['df1']
df2 = store['df2']


## a function to create word sets for each text
def make_wordsets():
    return lambda x: map(lambda y: re.sub('[^a-zA-Z0-9\n\ ]', '', y.strip()), x)

	
## a function to return the Jaccard similarity for any two sets
def calcJaccardSimilarity(wordset1, wordset2):
    return len(set(wordset1).intersection(set(wordset2))) / float(len(set(wordset1).union(set(wordset2))))

# saving the created word sets in sets
df1['sets'] = df1.text.str.lower().str.split().apply(make_wordsets())


# text to lower case no special characters
df1['text'] = df1.text.str.lower().str.strip().apply(lambda x: re.sub('[^a-zA-Z0-9\n\ ]', '', x))

# print the Jaccard similarity for articles in loc[0] and loc[1], for example
print calcJaccardSimilarity(set(df1.loc[0]['sets']), set(df1.loc[1]['sets']))

# print Jaccard similarity for Germany and Europe article
print 'Jaccard similarity for Germany and Europe article:', calcJaccardSimilarity(set(df1[df1.name=="Germany"].sets.item()), set(df1[df1.name=="Europe"].sets.item()))

# a function to create a set of all unique words in the file
def makeoneset(dataframe):
    results = set()
    dataframe.apply(results.update)
    return results
aset = makeoneset(df1.sets)

# idf
start_time = time.time()
dictionary = dict()
counter = 0
for word in list(aset):
    dictionary[word] = round(math.log(len(aset) / float(len(df1[df1.text.str.contains(word)]))), 2)
    counter += 1
    if counter == 100:
        print("--- %s seconds ---" % (time.time() - start_time))
        break

# idf
# start_time = time.time()
# dictionary2 = dict()
# counter = 0
# for word in list(aset):
    # dictionary2[word] = round(math.log(len(aset) / float(sum(df1.sets.apply(lambda x: 1 if word in x else 0)))), 2)
    # counter += 1
    # if counter == 100:
        # print("--- %s seconds ---" % (time.time() - start_time))
        # break

# tf
def makeDict(setofwords):
    counts = dict()
    for i in setofwords:
      counts[i] = counts.get(i, 0) + 1
    return counts

# function to calculate tfidf (takes in two dictionaries)
def tfidf(x, y):
    return dict((k, v * x[k]) for k, v in y.items() if k in x)


df1['tfidf'] = df1.sets.apply(lambda x: tfidf(makeDict(x), dictionary))










## NOTES ##


# fix the shape of the series for multipication (document vectors make same size with adding zeroes to no words)
# def fixShape(doc):
    # if doc.size != 10:
        # for i in xrange(abs(doc.size-len(dictionary))): # len(aset)
           # doc = doc.set_value(i, i*0)
    # return doc
# d = {'idf' :pd.Series([0], index=aset)}
# r1 = pd.DataFrame(pd.Series(dictionary))
# d = {'doc3' : pd.Series([0], index=dictionary)}
# r = pd.DataFrame(d)
# r.insert(r.columns.size, df1.loc[(r.columns.size - 1)].name, [1 if d[(r.index)] else 0]) ## df1.loc[1661].tf[str(r.index.values)]
# print r1

# def calculateCosineSimilarity(tfIdfDict1, tfIdfDict2):
    # print('similarity between {} and {}'.format(tfIdfDict1, tfIdfDict2))
    # return round(dicOneMultiDicTwo(tfIdfDict1, tfIdfDict2) / (lengthofavector(tfIdfDict1) * lengthofavector(tfIdfDict2)), 2)

# a function to get the similarity of two dictionaries
# def dicOneMultiDicTwo(dictt1, dictt2):
    # return sum(fixShape(pd.Series(dictt1)).values * fixShape(pd.Series(dictt2)).values)

# def lengthofavector(dict11):
    # return round(math.sqrt(sum((val**2) for val in dict11.values())), 2)

# len(dictionary)
# print df1[df1.text.str.contains("woody")].name

# print calculateCosineSimilarity(dict1, dict2)
# print calculateCosineSimilarity(dict1, dict3)

# dict1 = {'how': 5, 'are': 15, 'inanimate': 10}
# dict2 = {'hi': 6, 'it': 10, 'is': 17}
# dict3 = {'hello': 3, 'this': 2, 'is': 2, 'me': 19}

# import csv
# def writeintodic(diction):
    # with open('dict.csv', 'wb') as csv_file:
        # writer = csv.writer(csv_file)
        # for key, value in diction.items():
           # writer.writerow([key, value])

# writeintodic(dictionary)

# def chunker(seq, size):
    # return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

# dictt = dict()
# for group in chunker(list(aset), 5):
    # for gr in group:
        # dictt[gr] = sum(df1.text.apply(lambda x: 1 if gr in x else 0))

# def finddf(listtext , theword):
    # if theword in listtext:
        # return 1
    # else:
        # return 0
    # x = sum(df1.text.apply(lambda x: finddf(x, aword)))

# count = {}
# count['the'] = sum(df1.text.apply(lambda x: finddf(x, "germany")))

# print count

# import random
# bset = aset
# x1 = len(bset) / 250
# set1 = set(random.sample(bset, x1))
# dictt = dict()
# for aword in set1:
    # dictt[aword] = sum(df1.text.apply(lambda x: 1 if aword in x else 0))

# import random

# pool = aset # your 240 elements here
# slen = len(pool) / 10 # we need 3 subsets
# set1 = set(random.sample(pool, slen)) # 1st random subset
# pool -= set1
# set2 = set(random.sample(pool, slen)) # 2nd random subset
# pool -= set2
# set3 = pool # 3rd random subset

# print x1
# print len(set1)

# if we had to use pd.Series
# def calcJaccardSimilaritySeries(l, m):
    # return pd.Series(np.intersect1d(l,m)).size / float(pd.Series(np.union1d(l,m)).size)
# l = df1[df1.name=="Germany"].text.item()
# m = df1[df1.name=="Europe"].text.item()
# calcJaccardSimilaritySeries(l,m)

# store.close()