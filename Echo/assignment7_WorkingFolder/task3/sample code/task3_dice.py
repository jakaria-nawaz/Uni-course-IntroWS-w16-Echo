# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 16:23:49 2016

ToDo:
    1. simple dice method ( random number) # done
    2. roll two dices                       # done
    3. sum up both dices                   # done
    4. calc frequencies of dice sum        # done
    5. plot histogram with frequencies
    6. calc plot cdf
    7.1 median sum of two dice sides.
    7.2 mark point on plot
    8.1 probability of dice sum to be equal or less than 9. 
    8.2 mark on plot
    9. repeat simulation second time, compute max point-wise distance of both cdf
    10. repeat sim (2times) with n =1000 and compute the maximum oint-wise distance of cfds
    11. conclusion you can draw from inc the # of steps in sim
"""

import random
import collections

import matplotlib.pyplot as plt
import numpy as np

#########################################
# def dice() 
# -simple dice method
# return: a random number between 1 and 7
#########################################
def dice():
    return random.randrange(1,7,1)

###########################################################
# def rollDices(numberOfTimes) 
# -method to call dice method for a specific "numberOfTimes
# -sums up the returned number from dice method
# -add the sum to a list
# return: list with the "sums per throw"
###########################################################
def rollDices(numberOfTimes):
    sumPerThrow = []
    n = 0
    while n < numberOfTimes:
        n+=1
        sumPerThrow.append(dice()+dice())
    return sumPerThrow

#########################################
# def plotHistogram
# 
# 
#########################################
def plotHistogram():
    rng = np.random.RandomState(10)  # deterministic random data
    
    a = np.hstack((rng.normal(size=1000),
               rng.normal(loc=5, scale=2, size=1000)))
    plt.hist(a, bins='auto')  # plt.hist passes it's arguments to np.histogram
    plt.title("Histogram with 'auto' bins")
    plt.show()
'''
def plotHistogram3(values, keys):
    print(keys)
    y_pos = np.arange(len(keys))
    print(y_pos)
    performance = [counter[k] for k in keys]
    pefo = [for k in keys]
    print(performance)
    print(pefo)
    plt.bar(y_pos, performance, align='center')
    plt.show()

#def plotHistogram2(values):
    #for val in values:
       #print(val)
    #plt.hist(a, bins='auto')  # plt.hist passes it's arguments to np.histogram
    #plt.title("Histogram with 'auto' bins")
    #plt.show()
def plotHistogram2(values, keys):
    # Counter data, counter is your counter object
    keys = counter.keys()
    y_pos = np.arange(len(keys))
    # get the counts for each key, assuming the values are numerical
    performance = [counter[k] for k in keys]
    # not sure if you want this :S
    error = np.random.rand(len(keys))
    
    plt.bar(y_pos, performance, xerr=error, align='center', alpha=0.4)
    plt.yticks(y_pos, keys)
    plt.xlabel('Counts per key')
    plt.title('How fast do you want to go today?')
    
    plt.show()
'''
#################################################
# Main
#################################################    
print("\n#\n")
sumDiceList = rollDices(100)
print("sumDiceList: " + str(sumDiceList))

print("\n#\n")
counter=collections.Counter(sumDiceList)
print("collections.Counter: " + str(counter))

print("\n#\n")
print("counter.values : " + str(counter.values()))

print("\n#\n")
print("counter.keys : " + str(counter.keys()))

#plotHistogram3(counter.values(), counter.keys())
#plotHistogram2(counter.values)