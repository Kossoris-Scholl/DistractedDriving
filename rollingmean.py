import pandas as pd

def rolling_mean(file, window_size):
    df = pd.read_csv(file)

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

    return df

path = '../NormalizedData/'

fileNames = []

omitted = [30, 37, 48, 49, 52, 53, 56, 57, 58, 59, 63, 65, 67, 69, 70, 71, 72, 78, 85, 87]
for x in range(1, 10):
    fileNames.append("Normalized_T00" + str(x) + ".csv")
for x in range(10, 89):
    if x not in omitted:
        fileNames.append("Normalized_T0" + str(x) + ".csv")

window_size = int(input('Enter a window size: '))

for file in fileNames:

    originalName = file
    file = path + file

    csvFileName = 'Averaged_' + originalName

    df = rolling_mean(file, window_size)
    df.to_csv('../RollingAverageData/' + csvFileName, sep=',')