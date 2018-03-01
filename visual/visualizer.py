import matplotlib.pyplot as plt
import config
import csv
import numpy as np
import sys

######## Configure File Info Here #########
filenum = "022"
columnCompare = "Perinasal.Perspiration"
###########################################

fig, ax = plt.subplots()
configs = config.Config()
columnData = {}

if int(filenum) in configs.omitted:
    print("Invalid File Number!")
    sys.exit()

if columnCompare not in configs.columnNames:
    print("Invalid Column Name!")
    sys.exit()

file = configs.localPathAverage + "Averaged_Normalized_T" + filenum + ".csv"

for columnName in configs.columnNames:
    columnData[columnName] = []

dictReader = csv.DictReader(open(file, 'rt'), fieldnames=configs.columnNames,
                            delimiter=',', quotechar='"')

for row in dictReader:
    for key in row:
        columnData[key].append(row[key])

start = 1
count = 0
prevTime = 1

for i in range(1, len(columnData["Time"])):
    if int(columnData["Time"][i]) < prevTime and count != 0:
        print("start: " + str(start) + "\nend: " + str(i) + "\n")
        x = list(map(int, columnData["Time"][start:i-1]))
        y = list(map(float, columnData[columnCompare][start:i-1]))
        c = np.array([]);

        for data in columnData["Stimulus"][start:i-1]:
            if data != '0':
                c = np.append(c, 1);
            else:
                c = np.append(c, 0);

        plt.scatter(x,y, label='skitscat', c=c, s=25, marker="o")

        plt.xlabel('Time')
        plt.ylabel(columnCompare)
        plt.title(columnCompare + " v " + "Time\nRun " + str(count))
        plt.legend()
        plt.show()
        start = i
        count += 1
        prevTime = 1

    if count == 0:
        count = 1

    prevTime += 1