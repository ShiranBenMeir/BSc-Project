import matplotlib.pyplot as plt
from statistics import mean
import xlrd
import csv

def filterData():
    namesList=[]
    wb = xlrd.open_workbook("locations.xlsx")
    i = 0;
    while i < 5:
        sheet = wb.sheet_by_index(i)
        for k in range(0, sheet.nrows):
            protName = sheet.row_values(k)[0]
            protLoc = sheet.row_values(k)[1]
            if (protLoc == 'cytoplasm' or protLoc == 'nucleus'):
                if protName not in namesList:
                    namesList.append(protName)
        i = i + 1
    return namesList


def ReadingFromProtFeatures(namesList,fileName):
    dictByName = {}

    wb = xlrd.open_workbook(fileName)
    i = 0;
    while i < 5:
        sheet = wb.sheet_by_index(i)
        for k in range(0, sheet.nrows):
            protName = sheet.row_values(k)[0]
            protLoc = sheet.row_values(k)[1]
            if protName in namesList:
                if protName in dictByName:
                    tempList = dictByName[protName]
                    tempList.append(protLoc)
                    dictByName[protName] = tempList
                else:
                    tempList = []
                    tempList.append(protLoc)
                    dictByName[protName] = tempList
        i = i + 1
    return dictByName


def ReadingFromProteinStability(namesList):
    temp = []
    testDict={}
    stabilityDict = {}
    avoidDupList = []
    with open('protein_stability.csv') as csvDataFile:
        data = list(csv.reader(csvDataFile))
        for lineNum in range(1, len(data)):
            protName = data[lineNum][1]
            stability = data[lineNum][4]
            if protName in namesList:
                if protName not in avoidDupList:
                    stabilityDict[protName] = stability
                    avoidDupList.append(protName)
    return stabilityDict


def intersectTwoDict(dictByName,stabilityDict):
    filteredNameDict = {}
    intersectProt = list(set(stabilityDict.keys()).intersection(set(dictByName.keys())))
    for filteredProtName in intersectProt:
        filteredNameDict[filteredProtName] = [dictByName[filteredProtName], stabilityDict[filteredProtName]]
    return filteredNameDict




def MapByFeature(filteredNameDict):
    dictByLoc={}
    for protName in filteredNameDict:
        for loc in filteredNameDict[protName][0]:
            if loc in dictByLoc:
                temp = dictByLoc[loc]
                temp.append(float(filteredNameDict[protName][1]))
                dictByLoc[loc] = temp
            else:
                temp = []
                temp.append(float(filteredNameDict[protName][1]))
                dictByLoc[loc] = temp

    return dictByLoc

def meanOfMeans(dictByLoc):
    meanDictByLoc={}
    sum=[]
    for x in dictByLoc:
        meanDictByLoc[x]=mean(dictByLoc[x])

    for x in meanDictByLoc:
        sum.append(meanDictByLoc[x])

    meanSum= mean(sum)
    print("mean: ", meanSum)



def main():
    namesList=filterData()
    dictByName=ReadingFromProtFeatures(namesList,fileName="pathways.xlsx")
    stabilityDict=ReadingFromProteinStability(namesList)
    filteredNameDict=intersectTwoDict(dictByName, stabilityDict)
    dictByLoc=MapByFeature(filteredNameDict)
    meanOfMeans(dictByLoc)

    lst=['Cell cycle Cell cycle (generic schema)', 'Wnt signaling network', 'Nanog in Mammalian ESC Pluripotency',
         'PD-1 signaling', 'Selenium Micronutrient Network', 'Ubiquitination Cascade Pathway', 'DNA methylation',
         'Negative feedback regulation of MAPK pathway']
    lst2 = ['chemokine receptor activity', 'oxygen binding', 'ubiquitin conjugating enzyme binding',
            'AMP-activated protein kinase activity','protein phosphatase activator activity', 'protein kinase activator activity',
            'unfolded protein binding', 'U1 snRNA binding', 'U6 snRNA binding', 'phospholipase inhibitor activity']


    for x in dictByLoc:
        if x in lst:
            for y in dictByLoc[x]:
                for key, val in stabilityDict.items():
                    val = float(val)
                    if float(val) == y:
                        print(x, key)


    return dictByLoc

if __name__ == "__main__":
    main()