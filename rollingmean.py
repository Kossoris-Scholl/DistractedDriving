import csv
import pandas as pd

def rolling_mean(columnData, window_size):
    df = pd.DataFrame(data=columnData)
    df['Heart.Rate'] = df.rolling(window_size).mean()
    # print(df)
    return df

path = '../NormalizedData/'

fileNames = []

omitted = [30, 37, 48, 49, 52, 53, 56, 57, 58, 59, 63, 65, 67, 69, 70, 71, 72, 78, 85, 87]
for x in range(1, 10):
    fileNames.append("Normalized_T00" + str(x) + ".csv")
for x in range(10, 89):
    if x not in omitted:
        fileNames.append("Normalized_T0" + str(x) + ".csv")

columnNames = ["Time", "Drive", "Stimulus", "Failure", "Palm.EDA", "Heart.Rate", "Breathing.Rate",
               "Perinasal.Perspiration", "Speed", "Acceleration", "Brake", "Steering", "LaneOffset",
               "Lane.Position", "Distance", "Gaze.X.Pos", "Gaze.Y.Pos", "Lft.Pupil.Diameter",
               "Rt.Pupil.Diameter"]

window_size = int(input('Enter a window size: '))

for file in fileNames:

    originalName = file
    file = path + file
    columnData = {}

    for columnName in columnNames:
        columnData[columnName] = []

    dictReader = csv.DictReader(open(file, 'rt'), fieldnames=columnNames,
                                delimiter=',', quotechar='"')

    for row in dictReader:
        for key in row:
            columnData[key].append(row[key])

    keys = columnNames
    csvFileName = 'Averaged_' + originalName

    df = rolling_mean(columnData, window_size)
    df.to_csv('../RollingAverageData/' + csvFileName, sep=',')