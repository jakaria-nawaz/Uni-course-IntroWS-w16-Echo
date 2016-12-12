import random
import numpy as np
import matplotlib.pyplot as plt

def dice_roll():
    global dice1Result
    dice1Result.append(random.randint(1,6))

    global dice2Result
    dice2Result.append(random.randint(1,6))

def drawHistogram(sumDiceResult):
    plt.hist(sumDiceResult)
    plt.title('Frequencies of sum results of Dice rolling')
    plt.ylabel('Frequencies')
    plt.xlabel('Different Sum Results')
    plt.grid('on')
    plt.show()

def drawCDF(sumDiceResult):
    sorted = np.sort(sumDiceResult)
    print(sorted)
    yvals = np.arange(len(sorted))/float(len(sorted))
    plt.plot(sorted, yvals)
    plt.grid('on')
    plt.show()

# def drawCDF2(sumDiceResult):
#     # evaluate the histogram
#     values, base = np.histogram(sumDiceResult, bins=40)
#     #evaluate the cumulative
#     cumulative = np.cumsum(values)
#     # plot the cumulative function
#     plt.plot(base[:-1], cumulative, c='blue')
#     #plot the survival function
#     #plt.plot(base[:-1], len(data)-cumulative, c='green')
#     plt.title('CDF Frequencies of sum results of Dice rolling')
#     plt.ylabel('CDF of Frequencies')
#     plt.xlabel('Sum Results')
#     plt.show()

def main():
    global dice1Result
    dice1Result = []

    global dice2Result
    dice2Result = []

    global sumDiceResult
    sumDiceResult = []

    for x in range(0, 100):
        dice_roll()

    sumDiceResult = [x + y for x, y in zip(dice1Result, dice2Result)]
    print(dice1Result)
    print(dice2Result)
    print(sumDiceResult)

    #Draw histogram
    drawHistogram(sumDiceResult)
    #Draw CDF
    drawCDF(sumDiceResult)
    #drawCDF2(sumDiceResult)


if __name__ == '__main__':
    main()
