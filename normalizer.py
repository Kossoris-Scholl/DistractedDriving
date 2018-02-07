import csv
import config
import sys

def normalizer(data):
    minHR = sys.maxsize
    maxHR = -1

    for hr in data:
        try:
            hr = float(hr)
            if hr != 0:
                if hr < minHR:
                    minHR = hr
                if hr > maxHR:
                    maxHR = hr
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
    originalName = file
    file = configs.localPath + file

    columnData = {}

    for columnName in configs.columnNames:
        columnData[columnName] = []

    dictReader = csv.DictReader(open(file, 'rt'), fieldnames=configs.columnNames,
                                delimiter=',', quotechar='"')

    for row in dictReader:
        for key in row:
            columnData[key].append(row[key])


    columnData["Palm.EDA"] = normalizer(columnData["Palm.EDA"])
    columnData["Heart.Rate"] = normalizer(columnData["Heart.Rate"])
    columnData["Breathing.Rate"] = normalizer(columnData["Breathing.Rate"])
    columnData["Perinasal.Perspiration"] = normalizer(columnData["Perinasal.Perspiration"])
    columnData["Lft.Pupil.Diameter"] = normalizer(columnData["Lft.Pupil.Diameter"])
    columnData["Rt.Pupil.Diameter"] = normalizer(columnData["Rt.Pupil.Diameter"])
    
    csvFileName = 'Normalized_' + originalName

    keys = configs.columnNames
    with open('../NormalizedData/'+csvFileName, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerows(zip(*[columnData[key] for key in keys]))

