import time
import pandas as pd
import matplotlib.pyplot as plt


def readFile(x):
    lines = []
    for line in open(x):
        lines.append(line)
    return lines
	
computer = readFile('computer.txt')
# using a sample of 100 articles only
articles = readFile('articles-sample.txt')

computerwords = []
for computerwrds in computer:
    computerwords.append(computerwrds.split('\n')[0])

# def wordstring(x):
#     return filter(lambda c: c.isalpha(), x)

start_time = time.time()
dictionry = {}
wordscomp = {}
num = 1
for article in articles:
    matchedwords = []
    for word in article.split():
        l = filter(lambda c: c.isalpha(), word)
        if l in computerwords:
            matchedwords.append(l)
    if len(matchedwords) > 2:
        dictionry[num] = 1
    else:
        dictionry[num] = 0
    wordscomp[num] = len(matchedwords)
    num += 1
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()

fd2 = pd.Series(dictionry)
print 'The average amount of computer science articles in all articles is', fd2.mean()
fd = pd.Series(wordscomp)
print 'The average amount of computer science words in all articles', fd.mean()

start_time = time.time()
fd.plot()
fd.mean()
plt.title('The distribution of Computer Science terms in articles')
plt.ylabel('Frequency of Computer Science terms')
plt.xlabel('Articles names(numbers refer to line number)')
plt.show()
print("--- %s seconds ---" % (time.time() - start_time))

