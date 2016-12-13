import random
import numpy as np
import matplotlib.pyplot as plt

def dice_roll():
    global dice1Result
    dice1Result.append(random.randint(1,6))

    global dice2Result
    dice2Result.append(random.randint(1,6))

def drawHistogram(sumDiceResult,n,rn):
    plt.hist(sumDiceResult)
    plt.title('Frequencies of sum results of Dice rolling')
    plt.title('Frequencies of sum results of Dice rolling for sample amount %d and simulation %d'%(n,rn))
    plt.ylabel('Frequencies')
    plt.xlabel('Sum Results')
    plt.grid('on')

    #plt.switch_backend('TkAgg')
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()

#http://stackoverflow.com/questions/3209362/how-to-plot-empirical-cdf-in-matplotlib-in-python
def drawCDF(sumDiceResult,n,rn):
    sorted1 = np.sort(sumDiceResult)
    theMedian = np.median(sorted1)

    print("Median val using np: ", theMedian)
    print("Median val manually: ", sorted1[50])
    totalNum9 = sum(i <= 9 for i in sorted1)
    totalNum9per = ((totalNum9*100)/100)/100
    print("Probability of dice sum to be equal or less than 9: ",totalNum9per)
    yvals = np.arange(len(sorted1))/float(len(sorted1))
    plt.plot(sorted1, yvals)
    plt.plot((0, 12), (.5, .5))
    plt.plot((9, 9), (0, 1))
    plt.plot((theMedian,theMedian), (0, .5))
    plt.plot((0,12), (totalNum9per, totalNum9per))
    plt.legend(['CDF', '50%', '<=9','Median','Percentage of <=9',], loc='lower right')
    plt.gca().set_color_cycle(['blue', 'green', 'red', 'orange','yellow'])

    plt.annotate('Median: %d'%theMedian, (theMedian,.5),xytext=(0.7, 0.7),arrowprops=dict(arrowstyle='->'))
    plt.annotate('Probability (<=9): %s'%totalNum9per, (9,totalNum9per),xytext=(1, 0.9),arrowprops=dict(arrowstyle='->'))

    plt.title('CDF of dice sum frequency for sample amount %d and simulation %d'%(n,rn))
    plt.ylabel('Probability')
    plt.xlabel('Sum Results (x)')
    plt.grid('on')

    #plt.switch_backend('TkAgg')
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

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
    global sumDiceResult2
    sumDiceResult2 = []

    #Simulation 1
    for x in range(0, 100):
        dice_roll()

    sumDiceResult = [x + y for x, y in zip(dice1Result, dice2Result)]
    # print(dice1Result)
    # print(dice2Result)
    # print(sumDiceResult)

    print('Results for simulation 1')
    #Draw histogram
    drawHistogram(sumDiceResult,100,1)
    #Draw CDF
    drawCDF(sumDiceResult,100,1)
    #drawCDF2(sumDiceResult)

    #Simulation 2
    global dice1Result
    dice1Result = []
    global dice2Result
    dice2Result = []

    for x in range(0, 100):
        dice_roll()

    sumDiceResult2 = [x + y for x, y in zip(dice1Result, dice2Result)]

    print('Results for simulation 2')
    #Draw histogram
    drawHistogram(sumDiceResult2,100,2)
    #Draw CDF
    drawCDF(sumDiceResult2,100,2)
    #drawCDF2(sumDiceResult)

if __name__ == '__main__':
    main()
