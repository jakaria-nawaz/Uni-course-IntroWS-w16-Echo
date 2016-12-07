#!python2
import time
import pandas as pd
import matplotlib.pyplot as plt


def readFile(x):
    lines = []
    for line in open(x):
        lines.append(line)
    return lines

computer = readFile('computer.txt')
# using a sample of 500 articles only
articles = readFile('articles')

computerwords = []
for computerwrds in computer:
    computerwords.append(computerwrds.split('\n')[0])

start_time = time.time()
dictionry = {}
wordscomp = {}
num = 1
for article in articles:
    matchedwords = []
    allwords = len(article.split())
    for word in article.split():
        l = filter(lambda c: c.isalpha(), word)
        if l in computerwords:
            matchedwords.append(l)
    dictionry[num] = len(matchedwords)
    try:
        wordscomp[num] = float(len(matchedwords))/allwords
    except:
        pass
    num += 1
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
fd = pd.Series(wordscomp)
print 'The average amount of computer science terms in all articles in the data set: ', fd.mean()
fd.plot()
plt.title('The average distribution of Computer Science terms in each article')
plt.ylabel('The average frequency of Computer Science terms')
plt.xlabel('Articles names(numbers refer to line number)')
plt.show()
print("--- %s seconds ---" % (time.time() - start_time))
