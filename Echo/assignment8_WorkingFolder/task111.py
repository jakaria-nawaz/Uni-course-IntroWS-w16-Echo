import pandas as pd
import numpy as np
import re


## a function to create word sets for each text
def make_wordsets():
    return lambda x: map(lambda y: re.sub('[^a-zA-Z0-9\n\ ]', '', y.strip()), set(x))


## a function to return the Jaccard similarity for any two sets
def calcJaccardSimilarity(wordset1, wordset2):
    return len(wordset1.intersection(wordset2)) / float(len(wordset1.union(wordset2)))


store = pd.HDFStore('store.h5')
df1 = store['df1']
df2 = store['df2']
	
# saving the created word sets in the text column (this will change the content of store.h5)
df1['text'] = df1.text.str.lower().str.split().apply(make_wordsets())

# print the Jaccard similarity for articles in loc[0] and loc[1], for example
print calcJaccardSimilarity(set(df1.loc[0]['text']), set(df1.loc[1]['text']))

# print Jaccard similarity for Germany and Europe article
print 'Jaccard similarity for Germany and Europe article:', calcJaccardSimilarity(set(df1[df1.name=="Germany"].text.item()), set(df1[df1.name=="Europe"].text.item()))

## if we had to use pd.Series
# def calcJaccardSimilaritySeries(l, m):
    # return pd.Series(np.intersect1d(l,m)).size / float(pd.Series(np.union1d(l,m)).size)
# l = df1[df1.name=="Germany"].text.item()
# m = df1[df1.name=="Europe"].text.item()
# calcJaccardSimilaritySeries(l,m)

store.close()
