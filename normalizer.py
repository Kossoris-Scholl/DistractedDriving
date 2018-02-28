import csv
import config
import sys
import pandas as pd

def normalizer(data, key):
    minimum = float(sys.maxsize)
    maximum = float(-1)

    for value in data:
        try:
            value = float(value)
            if value < minimum:
                minimum = value
            if value > maximum:
                maximum = value
        except ValueError:
            pass

    for i in range(len(data)):
        try:
            data[i] = float(data[i])
            if data[i] == 0:
                data[i] = -1
            elif maximum == minimum: #look at interpolated t007 for an example of why this is the case we could just make a req that all values must be there to keep the row
                data[i] = 1
            else:
                data[i] = (data[i] - minimum) / (maximum - minimum)
        except ValueError:
            if data[i] != key:
                data[i] = -1
            else:
                pass

    return data

configs = config.Config()


for file in configs.fileNames:
    print(file)
    originalName = file
    file = configs.localPath + file
    keys = configs.columnNames
    columnData = {}

    for columnName in configs.columnNames:
        columnData[columnName] = []

    df = pd.read_csv(file)
    df = df.interpolate(limit = 10)
    df = df.dropna(thresh = 10) #at least ten (minus 4) values required in a row to keep the row
    df.to_csv('../InterpolatedData/Interpolated_' + originalName, index=False)

    dictReader = csv.DictReader(open('../InterpolatedData/Interpolated_' + originalName, 'rt'), fieldnames=configs.columnNames,
                                delimiter=',', quotechar='"')

    for row in dictReader:
        for key in row:
            columnData[key].append(row[key])


    for i in range(4,19):
        columnData[keys[i]] = normalizer(columnData[keys[i]], keys[i])


    with open('../NormalizedData/Normalized_' + originalName, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerows(zip(*[columnData[key] for key in keys]))

