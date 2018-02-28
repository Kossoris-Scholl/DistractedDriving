import pandas as pd
import config
import csv

def rolling_mean(file, columnData, window_size):

    current = 1
    first_run = True
    for i in range(1, len(columnData["Time"])):
        if int(columnData["Time"][i]) == 1:
            df = pd.read_csv(file, skiprows=current, nrows=i-current, names = ["Time", "Drive",	"Stimulus", "Failure", "Palm.EDA", "Heart.Rate", "Breathing.Rate",
                "Perinasal.Perspiration", "Speed", "Acceleration", "Brake", "Steering", "LaneOffset",
                "Lane.Position", "Distance", "Gaze.X.Pos", "Gaze.Y.Pos", "Lft.Pupil.Diameter", "Rt.Pupil.Diameter"])
            df['Palm.EDA'] = df.rolling(window_size).mean()['Palm.EDA']
            df['Heart.Rate'] = df.rolling(window_size).mean()['Heart.Rate']
            df['Breathing.Rate'] = df.rolling(window_size).mean()['Breathing.Rate']
            df['Perinasal.Perspiration'] = df.rolling(window_size).mean()['Perinasal.Perspiration']
            df['Speed'] = df.rolling(window_size).mean()['Speed']
            df['Acceleration'] = df.rolling(window_size).mean()['Acceleration']
            df['Brake'] = df.rolling(window_size).mean()['Brake']
            df['Steering'] = df.rolling(window_size).mean()['Steering']
            df['LaneOffset'] = df.rolling(window_size).mean()['LaneOffset']
            df['Lane.Position'] = df.rolling(window_size).mean()['Lane.Position']
            df['Distance'] = df.rolling(window_size).mean()['Distance']
            df['Gaze.X.Pos'] = df.rolling(window_size).mean()['Gaze.X.Pos']
            df['Gaze.Y.Pos'] = df.rolling(window_size).mean()['Gaze.Y.Pos']
            df['Lft.Pupil.Diameter'] = df.rolling(window_size).mean()['Lft.Pupil.Diameter']
            df['Rt.Pupil.Diameter'] = df.rolling(window_size).mean()['Rt.Pupil.Diameter']
            current = i
            if first_run == True:
                first_run = False
                df2 = df
            else:
                df2 = pd.concat([df2, df])

    return df2

configs = config.Config()

window_size = int(input('Select a window size: '))

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

    df = rolling_mean(file, columnData, window_size)
    df.to_csv('../RollingAverageData/' + csvFileName, sep=',')