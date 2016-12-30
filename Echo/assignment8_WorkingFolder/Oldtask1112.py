import pandas as pd
import numpy as np
import time
import re

df1 = store['df1']
df2 = store['df2']

## a function to create word sets for each text
def make_wordsets():
    return lambda x: map(lambda y: re.sub('[^a-zA-Z0-9\n\ ]', '', y.strip()), x)

## a function to return the jaccard similarity for any two sets
def calcJaccardSimilarity(wordset1, wordset2):
    return len(set(wordset1).intersection(set(wordset2))) / float(len(set(wordset1).union(set(wordset2))))

# saving the created word sets in the text column
df1['text'] = df1.text.str.lower().str.split().apply(make_wordsets())

# print the jaccard similarity for articles in loc[0] and loc[1], for example
print calcJaccardSimilarity(set(df1.loc[0]['text']), set(df1.loc[1]['text']))

# print Jaccard similarity for Germany and Europe article
print 'Jaccard similarity for Germany and Europe article:', calcJaccardSimilarity(set(df1[df1.name=="Germany"].text.item()), set(df1[df1.name=="Europe"].text.item()))

# a function to create a set of all unique words in the file
def makeoneset(dataframe):
    results = set()
    dataframe.apply(results.update)
    return results
aset = makeoneset(df1.text)

# idf for the first 1000 words in the aset because of memory issues
start_time = time.time()
dictionary = dict()
counter = 0
for word in list(aset):
    dictionary[word] = sum(df1.text.apply(lambda x: 1 if word in x else 0))
    counter += 1
    if counter == 1000:
        print("--- %s seconds ---" % (time.time() - start_time))
        break

# tf
def makeDict(setofwords):
    counts = dict()
    for i in setofwords:
      counts[i] = counts.get(i, 0) + 1
    return counts

# function to calculate tdidf
def tfidf(x, y):
    return dict((k, v * x[k]) for k, v in y.items() if k in x)

df1.text.apply(lambda x: tfidf(makeDict(x), dictionary))




# ********NOTES********
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

# import random
# pool = aset # your 240 elements here
# slen = len(pool) / 10 # we need 3 subsets
# set1 = set(random.sample(pool, slen)) # 1st random subset
# pool -= set1
# set2 = set(random.sample(pool, slen)) # 2nd random subset
# pool -= set2
# set3 = pool # 3rd random subset


# if we had to use pd.Series
# def calcJaccardSimilaritySeries(l, m):
    # return pd.Series(np.intersect1d(l,m)).size / float(pd.Series(np.union1d(l,m)).size)
# l = df1[df1.name=="Germany"].text.item()
# m = df1[df1.name=="Europe"].text.item()
# calcJaccardSimilaritySeries(l,m)

store.close()
