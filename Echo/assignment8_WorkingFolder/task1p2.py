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

## a function to return the jaccard similarity for any two sets, reused from previous code
def calcJaccardSimilarity(outlinkset1, outlinkset2):
    return len(set(outlinkset1).intersection(set(outlinkset2))) / float(len(set(outlinkset1).union(set(outlinkset2))))

print 'Jaccard similarity for Germany and Europe out links:',calcJaccardSimilarity(df2[df2.name=="Germany"].out_links.item(), df2[df2.name=="Europe"].out_links.item())