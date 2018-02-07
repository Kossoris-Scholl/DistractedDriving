import csv
import config
import sys

def heartRateNormalizer(data):
    minHR = float(sys.maxsize)
    maxHR = float(-1)

    for hr in data:
        try:
            hr = float(hr)
            if hr != 0:
                if hr < minHR:
                    minHR = float(hr)
                if hr > maxHR:
                    maxHR = float(hr)
        except ValueError:
            pass

    for i in range(len(data)):
        try:
            data[i] = float(data[i])
            if data[i] == 0:
                data[i] = -1
            else:
                data[i] = (data[i] - minHR) / (maxHR - minHR)
        except ValueError:
            data[i] = -1

    return data

configs = config.Config()


for file in configs.fileNames:
    file = configs.localPath + file

    columnData = {}

    for columnName in configs.columnNames:
        columnData[columnName] = []

    dictReader = csv.DictReader(open(file, 'rt'), fieldnames=configs.columnNames,
                                delimiter=',', quotechar='"')

    for row in dictReader:
        for key in row:
            columnData[key].append(row[key])

    columnData["Heart.Rate"] = heartRateNormalizer(columnData["Heart.Rate"])


