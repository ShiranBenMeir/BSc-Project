import csv
from statistics import mean

import matplotlib.pyplot as plt
from matplotlib import colors
from pandas import np
import xlrd
from scipy.stats import stats

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


def ReadingFromProteinStability(namesList):
    stabilitySizeDict = {}
    with open('protein_stability.csv') as csvDataFile:
        data = list(csv.reader(csvDataFile))
        for lineNum in range(1, len(data)):
            # if data[lineNum][1] in namesList:
                if data[lineNum][2] != "" and data[lineNum][4] != "" and data[lineNum][3] != '1' and int(
                        data[lineNum][2]) < 3000:
                    protSize = float(data[lineNum][2]) / 3
                    stability = float(data[lineNum][4])
                    if protSize in stabilitySizeDict:
                        temp1 = stabilitySizeDict[protSize]
                        temp1.append(stability)
                        stabilitySizeDict[(protSize)] = temp1
                    else:
                        temp1 = []
                        temp1.append(stability)
                        stabilitySizeDict[protSize] = temp1
    return stabilitySizeDict

def SizeByStability(namesList):
    SizeStabilityDict = {}
    with open('protein_stability.csv') as csvDataFile:
        data = list(csv.reader(csvDataFile))
        temp1 = []
        for lineNum in range(1, len(data)):
            # if data[lineNum][1] in namesList:
                if data[lineNum][2] != "" and data[lineNum][4] != "" and data[lineNum][3] != '1' and int(
                        data[lineNum][2]) < 3000:
                    protSize = float(data[lineNum][2]) / 3
                    stability = float(data[lineNum][4])
                    stability= int(stability)
                    if stability in SizeStabilityDict:
                        temp1 = SizeStabilityDict[stability]
                        temp1.append(protSize)
                        SizeStabilityDict[(stability)] = temp1
                    else:
                        temp1=[]
                        temp1.append(protSize)
                        SizeStabilityDict[stability]=temp1
    for x in SizeStabilityDict:
        print(x, len(SizeStabilityDict[x]))
def main():
    x=[]
    y=[]
    namesList=filterData()
    SizeByStability(namesList)
    stabilitySizeDict=ReadingFromProteinStability(namesList)
    for k in stabilitySizeDict:
        for m in stabilitySizeDict[k]:
            x.append(k)
            y.append(m)

    print(len(x))
    print(len(y))
    import statsmodels.api as sm

    x = np.array(list(x))
    y = np.array(list(y))
    plt.scatter(x,y,s=1,c='royalblue')
    plt.xlabel('protein size (number of aa)', fontsize=10)
    plt.ylabel('stability score', fontsize=10)
    plt.title('stability vs. size', fontdict=None, loc='center', pad=None, fontsize=12)
    plt.yticks(np.arange(1, 6.5, 0.5))
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m * x + b, c= 'black')
    X2 = sm.add_constant(x)
    est = sm.OLS(y, X2)
    est2 = est.fit()
    print(est2.summary())

    plt.show()



if __name__ == "__main__":
    main()