# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 16:23:49 2016

ToDo:
    1. simple dice method ( random number) # done
    2. roll two dices                       # done
    3. sum up both dices                   # done
    4. calc frequencies of dice sum        # done
    5. plot histogram with frequencies      # done
    6. calc plot cdf                      # done
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

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import math


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
def plotHistogram(values, keys):
    listo = keys
    y_pos = np.arange(min(listo), max(listo)+1, 1)
    performance = values
    plt.bar(y_pos, performance, align='center')
    plt.show()



#########################################
# def cdf
# 
# 
#########################################   
def cdfPlot3(values,keys):
    sorted_data = np.cumsum(values)   
    y = np.arange(min(keys), max(keys)+1)
    plt.plot(y, sorted_data)
    
    plt.show()
 
def cdfPlot4(values,keys):
    sorted_data = np.cumsum(values)   
    markers_on = [0,1,2,3,4,5,6,7,8,9,10]
    print(values)
    print(keys)
    
    # draw a line at y=0.5 and x=0
    x = keys
    y = np.array([0.5,0.5,0.5,0.5,0.5,0.5,0.5, 0.5,0.5,0.5, 0.5])
    
 
    line = plt.plot(x,y)[0]
    line.set_clip_on(False)
    
    # draw a line at y= .... and x= median
    x2 = np.array([keys[5],keys[5],keys[5],keys[5],keys[5],keys[5],keys[5],keys[5],keys[5],keys[5],keys[5]])
    y2 = np.array([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    plt.plot(x2,y2)
    #plt.plot(xs, ys, '-gD', markevery=markers_on)
    y = np.arange(min(keys), max(keys)+1)
    plt.plot(y, sorted_data, markevery=markers_on, marker='o')
    plt.show()
    sumX = 0
    print("median")
    print(sorted_data[5])

    ## dist(x,y) = sqrt(x1^2 - y1^2) 
def calcDistance(x1, y1, x2, y2):
    distance = 0
    sqrt = 0
    distance = math.pow(x1 - x2, 2) + math.pow(y1 -y2, 2)
    sqrt = math.sqrt(distance)
    return sqrt    
    
    
#################################################
# Main
#################################################    
# roll the dice 100 times and create a list of values
sumDiceList = rollDices(100)

# create a directory (from sumDiceList) for number at keys and frequency at values
counter=collections.Counter(sumDiceList)

# Just check some values 
print("\n#\n")
print("sumDiceList: " + str(sumDiceList))
print("\n#\n")
print("collections.Counter: " + str(counter))
print("\n#\n")
print("counter.values : " + str(counter.values()))
print("\n#\n")
print("counter.keys : " + str(counter.keys()))


# save the elements from the frequency list in lists
keys = list(counter.keys())
values = list(counter.values())

# norm the values via list comprehension
normed = [i/sum(list(counter.values())) for i in list(counter.values())]

###### Plot with standard values #####
plotHistogram(values, keys)

##### Plot with normalize values ########
print("Normed values: " + str(normed))
plotHistogram(normed, keys)


######### Plot the cdf function ########
cdfPlot3(normed, keys)
cdfPlot4(normed, keys)

sumDiceList2 = rollDices(100)
counter2 = collections.Counter(sumDiceList2)
keys2 = list(counter2.keys())
values2 = list(counter2.keys())

normed2 = [i/sum(values2) for i in values2]
#print(normed2)

tmp = 0
y = 0
print("distance per point")
for x in normed:
    tmp = calcDistance(normed[y], keys[y], normed2[y], keys2[y])
    print("distance between point (" + str(y+1) + "): " + str(tmp))
    y+=1