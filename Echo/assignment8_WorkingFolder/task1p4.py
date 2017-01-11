import pandas as pd
import numpy as np
import time
import math
import re

store = pd.HDFStore('store.h5')
df1 = store['df1']
#Take a random article from df1
	#Take the index of the article
#If index a>50, take all articles whose index is in between a-50 and a+50 (This is the set y(100))
#Comare each y(100) with x and take index of most similar top 10 jaccard js(10), cosine cs(10).
#As we are working on Set Based Measure, we only need to identify distict elements in the set.
#Implement alogorithm of 'Set Based Measure'
