import csv
import matplotlib.pyplot as plt
from pandas import np
from statsmodels.compat import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import *
from statistics import mean




def one_plot(txtFileName):
    funcDict = {}
    temp = []
    with open(txtFileName, 'r') as f:
        for line in f:
            protName = line.split(None, 1)[0]
            protFunctions = line.split('sapiens\t', 1)[1]
            functionsList = protFunctions.split(',')
            for x in range(len(functionsList) - 1):
                temp.append(functionsList[x])
            funcDict[protName] = [temp]
            temp = []

    with open('protein_stability.csv') as csvDataFile:
        data = list(csv.reader(csvDataFile))
        for lineNum in range(1, len(data)):
            protName = data[lineNum][1]
            stability = float(data[lineNum][4])
            if (protName in funcDict and len(funcDict[protName]) == 1):
                funcDict[protName].append(stability)

    allFuncList = []
    for x in funcDict:
        for oneFunc in funcDict[x][0]:
            allFuncList.append(oneFunc)


    countDict = {}
    for lstElement in range(len(allFuncList)):
        protFunction = allFuncList[lstElement]
        counter = allFuncList.count(protFunction)
        if counter > 8:
            countDict[protFunction] = counter


    plt.bar(range(len(countDict)), list(countDict.values()),width=0.8, align='center')
    plt.xticks(range(len(countDict)), list(countDict.keys()))
    plt.xticks(rotation=90, fontsize=4)
    plt.axhline(24.87, c='g' )
    # plt.yticks(np.arange(0, 1500, 100))
    plt.ylabel('number of proteins', fontsize=10)
    plt.show()
    return countDict

def mixed_plot(lowCountDict, highCountDict,avgCountDict):
    highCompareDict={}
    lowCompareDict = {}
    xLabels=[]
    lowCompLst=[]
    highCompLst=[]
    avrgCompLst=[]
    # intersectProt = list(set(lowCountDict.keys()).intersection(set(highCountDict.keys())))
    intersectProt=list(set(lowCountDict.keys()).intersection(set(highCountDict.keys()), set(avgCountDict.keys())))
    for element in intersectProt:
        xLabels.append(element)
        lowCompLst.append(lowCountDict[element])
        highCompLst.append(highCountDict[element])
        avrgCompLst.append(avgCountDict[element])


    fig, ax = subplots()
    print(mean(lowCompLst))
    print(mean(highCompLst))
    print(mean(avrgCompLst))
    df = pd.DataFrame(np.c_[lowCompLst, highCompLst, avrgCompLst], index=xLabels)
    df.plot.bar(fontsize=6, ax=ax)
    ax.legend(["low stability", "high stability", "average stability"])
    plt.axhline(24.87, c='r', linewidth=0.5)
    plt.ylabel('number of proteins', fontsize=10)
    plt.show()


def uniqueElement(lowCountDict,highCountDict,avgCountDict):
    lst=[]
    for x in lowCountDict:
        lst.append(x)
    for x in highCountDict:
        lst.append(x)
    for x in avgCountDict:
        lst.append(x)

    lst=[x for x in lst if lst.count(x) == 1]
    # for x in lowCountDict:
    #     if x in lst:
    #         # print(x)
    #         k = x.split(':')
    #         print(k[1])
    # print('000000000000000000')
    # for x in avgCountDict:
    #     if x in lst:
    #         # print(x)
    #         k = x.split(':')
    #         print(k[1])
    print('9999999999999999999')
    for x in highCountDict:
        if x in lst:
            # print(x)
            k=x.split(':')
            print(k[1])





# lowCountDict=one_plot('lowFuncTXT.txt')
# highCountDict= one_plot('highFuncTXT.txt')
# avgCountDict= one_plot('avgFuncTXT.txt')
lowCountDict=one_plot('lowPathwayTXT.txt')
highCountDict= one_plot('highPathwayTXT.txt')
avgCountDict= one_plot('avgPathwayTXT.txt')
intersectProt= mixed_plot(lowCountDict,highCountDict,avgCountDict)
uniqueElement(lowCountDict,highCountDict,avgCountDict)
