import csv
import config
import sys

def normalizer(data, key):
    minimum = float(sys.maxsize)
    maximum = float(-1)

    for value in data:
        try:
            value = float(value)
            # if value != 0: plus indents
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

    columnData["Palm.EDA"] = normalizer(columnData["Palm.EDA"], keys[4])
    columnData["Heart.Rate"] = normalizer(columnData["Heart.Rate"], keys[5])
    columnData["Breathing.Rate"] = normalizer(columnData["Breathing.Rate"], keys[6])
    columnData["Perinasal.Perspiration"] = normalizer(columnData["Perinasal.Perspiration"], keys[7])
    columnData["Speed"] = normalizer(columnData["Speed"], keys[8])
    columnData["Acceleration"] = normalizer(columnData["Acceleration"], keys[9])
    columnData["Brake"] = normalizer(columnData["Brake"], keys[10])
    columnData["Steering"] = normalizer(columnData["Steering"], keys[11])
    columnData["LaneOffset"] = normalizer(columnData["LaneOffset"], keys[12])
    columnData["Lane.Position"] = normalizer(columnData["Lane.Position"], keys[13])
    columnData["Distance"] = normalizer(columnData["Distance"], keys[14])
    columnData["Gaze.X.Pos"] = normalizer(columnData["Gaze.X.Pos"], keys[15])
    columnData["Gaze.Y.Pos"] = normalizer(columnData["Gaze.Y.Pos"], keys[16])
    columnData["Lft.Pupil.Diameter"] = normalizer(columnData["Lft.Pupil.Diameter"], keys[17])
    columnData["Rt.Pupil.Diameter"] = normalizer(columnData["Rt.Pupil.Diameter"], keys[18])

    csvFileName = 'Normalized_' + originalName
    with open('../NormalizedData/'+csvFileName, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerows(zip(*[columnData[key] for key in keys]))

