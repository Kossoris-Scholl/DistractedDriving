import pandas as pd
import config
import csv

###function to take window average over the normalized data
def rolling_mean(file, columnData, window_size):

    keys = ["Time", "Drive", "Stimulus", "Failure", "Palm.EDA", "Heart.Rate", "Breathing.Rate",
                "Perinasal.Perspiration", "Speed", "Acceleration", "Brake", "Steering", "LaneOffset",
                "Lane.Position", "Distance", "Gaze.X.Pos", "Gaze.Y.Pos", "Lft.Pupil.Diameter", "Rt.Pupil.Diameter"]
    current = 1
    first_run = True
    for i in range(1, len(columnData["Time"])):
        if int(columnData["Time"][i]) == 1:
            df = pd.read_csv(file, skiprows=current, nrows=i-current, names = keys)
            for j in range(4, 19):
                df[keys[j]] = df.rolling(window_size).mean()[keys[j]]
            current = i
            if first_run == True:
                first_run = False
                df2 = df
            else:
                df2 = pd.concat([df2, df])

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
    df.to_csv('../RollingAverageData/' + csvFileName, sep=',')