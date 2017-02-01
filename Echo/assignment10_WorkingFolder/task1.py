# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 12:09:30 2017

@author: Hanadi
"""
import re
import csv
date_sys = dict()
hashtags = []
c = dict()
with open("onlyhash.data") as tsv:
    for line in csv.reader(tsv, dialect="excel", delimiter='\t'):
        tmp = []
        temp = line[2].strip().split('#')
        for tem in temp:
            x = re.sub('[^A-Za-z1-9]+', '', tem)
            if (x != ''):
                hashtags.append(x)
                tmp.append(x)
                if line[1] in date_sys.keys():
                    # a dictionary of dates as keys and values of list of hashtags on that date
                    date_sys[line[1]].append(x)
                else:
                    date_sys[line[1]] = tmp
dates = len(date_sys)
N = len(set(hashtags))
print "total number of dates: ", dates
print "total number of memes: ", N

from collections import Counter
import math
f = dict()
sys = dict()
for key, val in date_sys.items():
    counts = Counter(val)
    for val1 in counts:
        y = counts[val1]/float(N)
        f[val1] = round((y*math.log(y, 2)),3)
    # system entropy of hashtags on each date
    sys[key] = round( sum(f.values()) * (-1), 3)

import matplotlib.pylab as plt
from scipy.stats import rankdata
plt.scatter(rankdata(sys.keys()),rankdata(sys.values()))
plt.ylabel('Entropy')
plt.xlabel('Rank')
plt.show()
# we have made the system entropy per each day by finding the hashtags that were tweeted on that date and then used the entropy function on them, and each summation is the daily entropy of the tweeted hashtags
# the results are different because we have used a different entropy methodology than what is used in the author's plot
