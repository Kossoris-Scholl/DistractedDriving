import csv

import pandas as pd

from Processing import config


###function to take window average over the normalized data
def rolling_mean(file, columnData, window_size):

    keys = ["Time", "Drive", "Stimulus", "Failure", "Palm.EDA", "Heart.Rate", "Breathing.Rate",
                "Perinasal.Perspiration", "Speed", "Acceleration", "Brake", "Steering", "LaneOffset",
                "Lane.Position", "Distance", "Gaze.X.Pos", "Gaze.Y.Pos", "Lft.Pupil.Diameter", "Rt.Pupil.Diameter"]
    current = 1
    first_run = True
    prevTime = 1

    for i in range(1, len(columnData["Time"])):
        if int(columnData["Time"][i]) < prevTime or first_run or i == len(columnData["Time"])-1:
            df = pd.read_csv(file, skiprows=current, nrows=i-current, names = keys)
            for j in range(4, 19):
                df[keys[j]] = df.rolling(window_size).mean()[keys[j]]
            current = i
            if first_run == True:
                first_run = False
                df2 = df
            else:
                df2 = pd.concat([df2, df])
            prevTime = int(columnData["Time"][i])
        prevTime += 1
    return df2



configs = config.Config()

for file in configs.normalizedFileNames:

    originalName = file
    file = configs.localPathNormalized + file
    csvFileName = 'Averaged_' + originalName
    columnData = {}

    for columnName in configs.columnNames:
        columnData[columnName] = []

    dictReader = csv.DictReader(open(file, 'rt'), fieldnames=configs.columnNames,
                                delimiter=',', quotechar='"')

    for row in dictReader:
        for key in row:
            columnData[key].append(row[key])

    df = rolling_mean(file, columnData, configs.window_size)
    df = df.dropna()  # at least ten (minus 4) values required in a row to keep the row
    df.to_csv(configs.localPathAverage + csvFileName, sep=',', index=False)
