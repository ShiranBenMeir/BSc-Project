import csv


def readingFromDavid(fileName):
    funcDict={}
    with open(fileName, 'r') as f:
        for line in f:
            x = line.split('\t')
            protPVAL = float(line.split('\t')[4])
            protFunc = line.split('\t')[1]
            if len(x) > 1:
                protFunc = x[1]
            protNames = line.split('\t')[5]
            y = protFunc.split('~')
            if len(y) > 1:
                protFunc = y[1]
            z = protFunc.split(':')
            if len(z) > 1:
                protFunc = z[1]
            if protPVAL < 0.05:
                funcDict[protFunc]= protNames
    return funcDict


lowDict= readingFromDavid('lowDavidFunc.txt')
highDict= readingFromDavid('highDavidFunc.txt')
low={}
high={}
for key in lowDict:
    if key not in highDict:
        low[key]=lowDict[key]
for key in highDict:
    if key not in lowDict:
        high[key]=highDict[key]


for x in low:
    print(x)

#print("00000000000000000000000000000000000000000")

for x in high:
    print(x)

with open('highTEMP.csv', 'w', newline="") as csv_file:
    writer = csv.writer(csv_file)
    for key, value in high.items():
       writer.writerow([key, value])
