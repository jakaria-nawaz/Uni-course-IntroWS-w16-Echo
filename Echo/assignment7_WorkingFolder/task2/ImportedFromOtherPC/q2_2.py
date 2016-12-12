import random
import os
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
import operator
from collections import Counter

def wordF(fileName):
    file=open(fileName,"r+", encoding="utf8")
    wordcount={}
    for word in file.read().split():
        word = word.lower()
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
            #print (wordcount)
    #for k,v in wordcount.items():
        #print (k, v)
    return wordcount

def countFromFile(fileName):
    numberOfWords=0
    numberOfChar=0
    stat={}
    with open(fileName, 'r', encoding='utf8') as f:
        for contents in f:
            wordsList = contents.split()
            numberOfWords +=len(wordsList)
            for items in wordsList:
                #calculation each word length of the current list inside this loop
                numberOfChar+=len(items)
    stat[0] = numberOfChar
    stat[1] = numberOfWords
    return stat

def generateText(tp1,cdfdata,n,newFileName):
    lenOfDict = len(cdfdata)
    count = 0
    fullString = ""
    #indexVal = 0
    #print(tp1[30][0])
    while (count<=n):
        r = random.random()
        #print("Got R: ", r)
        for i in range(0,lenOfDict):
            if(r<=cdfdata[i]):
                fullString += str(tp1[i][0])
                #print((tp1[i][0]))
                break
        count = count + 1
    #print(fullString)
    with open(newFileName, 'a') as out:
        out.write(fullString)

def drawHistogramMulti(sortedMainDataFreq, sortedZipDataFreq, sortedUnipDataFreq):
    plt.gca().set_color_cycle(['blue', 'green', 'red'])
    plt.plot(sortedMainDataFreq)
    plt.plot(sortedZipDataFreq)
    plt.plot(sortedUnipDataFreq)
    plt.legend(['Main Data', 'Zip Generated', 'Unip Generated'], loc='upper right')
    plt.title('Word Frequency Diagram')
    plt.ylabel('Frequencies')
    plt.xlabel('Wordrank')
    plt.grid('on')
    plt.yscale('log')
    plt.xscale('log')
    plt.show()

def drawCDF(sortedMainDataFreq, sortedZipDataFreq, sortedUnipDataFreq):
    cumsumMain=np.cumsum(sortedMainDataFreq)
    normedcumsumMain=[x/float(cumsumMain[-1]) for x in cumsumMain]
    #wrank = {words[i]:i+1 for i in range(0,len(words))}

    cumsumZip=np.cumsum(sortedZipDataFreq)
    normedcumsumZip=[x/float(cumsumZip[-1]) for x in cumsumZip]

    cumsumUnip=np.cumsum(sortedUnipDataFreq)
    normedcumsumUnip=[x/float(cumsumUnip[-1]) for x in cumsumUnip]

    #k=ks_2samp(cumsumMain,cumsumUnip)
    #print("kolo: ",k)
    #print(normedcumsum)

    plt.plot(normedcumsumMain)
    plt.plot(normedcumsumZip)
    plt.plot(normedcumsumUnip)
    plt.xscale('log')
    plt.show()

def main():
    stat = countFromFile("asam.txt")
    numberOfChar = stat[0]
    numberOfWords = stat[1]

    zifp = { ' ': 0.17840450037213465, '1': 0.004478392057619917, '0': 0.003671824660673643, '3': 0.0011831834225755678, '2': 0.0026051307175779174, '5': 0.0011916662329062454, '4': 0.0011108979455528355, '7': 0.001079651630435706, '6': 0.0010859164582487295, '9': 0.0026071152282516083, '8': 0.0012921888323905763, '_': 2.3580656240324293e-05, 'a': 0.07264712490903191, 'c': 0.02563767289222365, 'b': 0.013368688579962115, 'e': 0.09688273452496411, 'd': 0.029857183586861923, 'g': 0.015076820473031856, 'f': 0.017232219565845877, 'i': 0.06007894642873102, 'h': 0.03934894249122837, 'k': 0.006067466280926215, 'j': 0.0018537015877810488, 'm': 0.022165129421030945, 'l': 0.03389465109649857, 'o': 0.05792847618595622, 'n': 0.058519445305660105, 'q': 0.0006185966212395744, 'p': 0.016245321110753712, 's': 0.055506530071283755, 'r': 0.05221605572640867, 'u': 0.020582942617121572, 't': 0.06805204881206219, 'w': 0.013964469813783246, 'v': 0.007927199224676324, 'y': 0.013084644140464391, 'x': 0.0014600810295164054, 'z': 0.001048859288348506}
    #for another probability set, let it be x1
    unip = {' ': 0.1875, 'a': 0.03125, 'c': 0.03125, 'b': 0.03125, 'e': 0.03125, 'd': 0.03125, 'g': 0.03125, 'f': 0.03125, 'i': 0.03125, 'h': 0.03125, 'k': 0.03125, 'j': 0.03125, 'm': 0.03125, 'l': 0.03125, 'o': 0.03125, 'n': 0.03125, 'q': 0.03125, 'p': 0.03125, 's': 0.03125, 'r': 0.03125, 'u': 0.03125, 't': 0.03125, 'w': 0.03125, 'v': 0.03125, 'y': 0.03125, 'x': 0.03125, 'z': 0.03125}

    sorted_zifp = sorted(zifp.items(), key=operator.itemgetter(0)) #Make tuples
    #for x1
    sorted_unip = sorted(zifp.items(), key=operator.itemgetter(0)) #Make tuples

    lenOfDict = len(sorted_zifp)
    #for x1
    lenOfDict_unip = len(sorted_unip)

    zifpCDFList = []
    #for x1
    unipCDFList = []

    for i in range(0,lenOfDict):
        if(i == 0):
            zifpCDFList.append(sorted_zifp[i][1])
        else:
            zipCDFap = zifpCDFList[i-1] + sorted_zifp[i][1]
            zifpCDFList.append(zipCDFap)

    #for x1
    for i in range(0,lenOfDict_unip):
        if(i == 0):
            unipCDFList.append(sorted_unip[i][1])
        else:
            unipCDFap = unipCDFList[i-1] + sorted_unip[i][1]
            unipCDFList.append(unipCDFap)


    generateText(sorted_zifp,zifpCDFList,numberOfChar,"ziptext.txt")
    #print("\n\n")
    generateText(sorted_unip,unipCDFList,numberOfChar,"uniptext.txt")

    mainDataFreq = wordF('asam.txt')
    zipDataFreq = wordF('ziptext.txt')
    unipDataFreq = wordF('uniptext.txt')

    list(mainDataFreq.values())

    #print("Frequency of words in main data set:\n", mainDataFreq)
    sortedMainDataFreq = list(mainDataFreq.values())
    sortedMainDataFreq = sorted(sortedMainDataFreq, reverse=True)
    #print("Frequency of words in main data set(values in list - sorted):\n", sortedMainDataFreq)
    #drawHistogram(sortedMainDataFreq)

    #print("\n\nFrequency of words in ZIP data set:\n", zipDataFreq)
    sortedZipDataFreq = list(zipDataFreq.values())
    sortedZipDataFreq = sorted(sortedZipDataFreq, reverse=True)
    #print("Frequency of words in ZIP data set(values in list - sorted):\n", sortedZipDataFreq)
    #drawHistogram(sortedZipDataFreq)

    #print("\n\nFrequency of words in UNIP data set:\n", unipDataFreq)
    sortedUnipDataFreq = list(unipDataFreq.values())
    sortedUnipDataFreq = sorted(sortedUnipDataFreq, reverse=True)
    #print("Frequency of words in UNIP data set(values in list - sorted):\n", sortedUnipDataFreq)
    #drawHistogram(sortedUnipDataFreq)

    drawHistogramMulti(sortedMainDataFreq, sortedZipDataFreq, sortedUnipDataFreq)
    drawCDF(sortedMainDataFreq, sortedZipDataFreq, sortedUnipDataFreq)

if __name__ == '__main__':
    main()
