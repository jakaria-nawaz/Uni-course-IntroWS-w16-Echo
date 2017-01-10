import pandas as pd
import numpy as np
import time
import math
import re

store = pd.HDFStore('store.h5')
df1 = store['df1']
df2 = store['df2']
def make_outlinkset():
     return lambda x: map(lambda y: re.sub('[^a-zA-Z0-9\n\ ]', '', y.strip()), x)

## a function to return the Jaccard similarity for any two sets
def calcJaccardSimilarity(wordset1, wordset2):
    return len(set(wordset1).intersection(set(wordset2))) / float(len(set(wordset1).union(set(wordset2))))

#print type(df2)
print df2.axes

#print df2[df2.name=="England"].out_links.item()

print 'Jaccard similarity for Germany and Europe out links:', calcJaccardSimilarity(df2[df2.name=="England"].out_links.item(), df2[df2.name=="Austria"].out_links.item())
