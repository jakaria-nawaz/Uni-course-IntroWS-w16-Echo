import pandas as pd
import numpy as np
import time
import math
import re

store = pd.HDFStore('store.h5')
df1 = store['df1']
df2 = store['df2']

### 1.1 Similarity of Text documents
## 1.1.1 Jaccard - Similarity on sets
# a function to create word sets for each text
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
print 'Jaccard similarity for article in loc[0] and article in loc[1]: ', calcJaccardSimilarity(set(df1.loc[0]['sets']), set(df1.loc[1]['sets']))

# print Jaccard similarity for Germany and Europe article
print 'Jaccard similarity for Germany and Europe article:', calcJaccardSimilarity(set(df1[df1.name=="Germany"].sets.item()), set(df1[df1.name=="Europe"].sets.item()))

## 1.1.2 TF-IDF with cosine similarity
# a function to create a set of all unique words in the file
def makeoneset(dataframe):
    results = set()
    dataframe.apply(results.update)
    return results
aset = makeoneset(df1.sets)

# idf (here was the runtime issue that I ran into and I couldn't think of another way to do it)
start_time = time.time()
dictionary = dict()
counter = 0
for word in list(aset):
    dictionary[word] = round(math.log(len(aset) / float(len(df1[df1.text.str.contains(word)]))), 2)
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

# saving tf scores as a dictionary for each document
df1['tf'] = df1.sets.apply(lambda x: makeDict(x))
print 'TF example for article loc[0]: ', df1.loc[0].tf

# function to calculate tfidf (takes in two dictionaries)
def tfidf(x, y):
    return dict((k, v * x[k]) for k, v in y.items() if k in x)

# saving tfidf dictionary
df1['tfidf'] = df1.sets.apply(lambda x: tfidf(makeDict(x), dictionary))
print 'TFIDF example for article in loc[0]: ', df1.loc[0].tfidf

# fix the shape of the series for multiplication (document vectors make same size with adding zeroes to no words)
def fixShape(doc):
    if doc.size != 10:
        for i in xrange(abs(doc.size-len(dictionary))): # len(aset)
           doc = doc.set_value(i, i*0)
    return doc

# a function to get the similarity of two dictionaries
def dicOneMultiDicTwo(dictt1, dictt2):
    return sum(fixShape(pd.Series(dictt1)).values * fixShape(pd.Series(dictt2)).values)

# a function to find the length of the vector
def lengthofavector(dict11):
    return round(math.sqrt(sum((val**2) for val in dict11.values())), 2)

# a function to calculate Cosine Similarity
def calculateCosineSimilarity(tfIdfDict1, tfIdfDict2):
    print('Cosine similarity between {} and {}'.format(tfIdfDict1, tfIdfDict2))
    return round(dicOneMultiDicTwo(tfIdfDict1, tfIdfDict2) / (lengthofavector(tfIdfDict1) * lengthofavector(tfIdfDict2)), 2)

print calculateCosineSimilarity(df1[df1.name=="Europe"].tfidf.item(), df1[df1.name=="Germany"].tfidf.item())

### 1.2 Similarity of Graphs
print 'Jaccard similarity for Germany and Europe out links:', calcJaccardSimilarity(df2[df2.name=="England"].out_links.item(), df2[df2.name=="Austria"].out_links.item())

store.close()
