import csv
import config
import sys

def normalizer(data, keys):
    minimum = float(sys.maxsize)
    maximum = float(-1)

    for value in data:
        try:
            value = float(value)
            if value != 0:
                if value < minimum:
                    minimum = float(value)
                if value > maximum:
                    maximum = float(value)
        except ValueError:
            pass

    for i in range(len(data)):
        try:
            data[i] = float(data[i])
            if data[i] == 0:
                data[i] = -1
            else:
                data[i] = (data[i] - minimum) / (maximum - minimum)
        except ValueError:
            if data[i] not in keys:
                data[i] = -1
            else:
                pass

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

    keys = configs.columnNames

    columnData["Palm.EDA"] = normalizer(columnData["Palm.EDA"], keys)
    columnData["Heart.Rate"] = normalizer(columnData["Heart.Rate"], keys)
    columnData["Breathing.Rate"] = normalizer(columnData["Breathing.Rate"], keys)
    columnData["Perinasal.Perspiration"] = normalizer(columnData["Perinasal.Perspiration"], keys)
    columnData["Lft.Pupil.Diameter"] = normalizer(columnData["Lft.Pupil.Diameter"], keys)
    columnData["Rt.Pupil.Diameter"] = normalizer(columnData["Rt.Pupil.Diameter"], keys)

    csvFileName = 'Normalized_' + originalName
    with open('../NormalizedData/'+csvFileName, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerows(zip(*[columnData[key] for key in keys]))

