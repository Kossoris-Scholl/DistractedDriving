import pandas as pd
from sklearn import metrics, neighbors

from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
import sklearn
import glob
import os
from Processing import config
import numpy as np

def knn(balanced=False):
    # Concatenate all the files from each person into one dataframe
    configs = config.Config()
    path = configs.localPathAverage
    df = pd.concat((pd.read_csv(f) for f in glob.glob(os.path.join(path, '*.csv'))))
    df.to_csv("concat.csv", sep=',', index=False)
    df['Stimulus'] = df['Stimulus'].replace([2, 3, 4, 5, 6], 1)

    if balanced:
        # Group by Stimulus column so we can access count of each type of stimulus (0 and 1)
        g = df.groupby('Stimulus')
        # Get equal count of each type of stimulus (0 or 1) in new dataframe g
        g = g.apply(lambda x: x.sample(g.size().min()).reset_index(drop=True))
        X = g[['Palm.EDA', 'Heart.Rate', 'Breathing.Rate', 'Perinasal.Perspiration', 'Speed', 'Acceleration', 'Brake',
               'Steering', 'LaneOffset', 'Lane.Position', 'Distance', 'Gaze.X.Pos', 'Gaze.Y.Pos', 'Lft.Pupil.Diameter',
               'Rt.Pupil.Diameter']]
        y = g['Stimulus']
    else:
        X = df[['Palm.EDA', 'Heart.Rate', 'Breathing.Rate', 'Perinasal.Perspiration', 'Speed', 'Acceleration', 'Brake',
                'Steering', 'LaneOffset', 'Lane.Position', 'Distance', 'Gaze.X.Pos', 'Gaze.Y.Pos', 'Lft.Pupil.Diameter',
                'Rt.Pupil.Diameter']]
        y = df['Stimulus']

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    X_train = X_train.values.reshape(-1,15)
    y_train = y_train.values.astype('int')

    ## Instantiate the model with 50 neighbors.
    knn = sklearn.neighbors.KNeighborsClassifier(n_neighbors=50)

    ## Fit the model on the training data.
    knn.fit(X_train, y_train)

    ## See how the model performs on the test data.
    print(knn.score(X_test.values.reshape(-1,15), y_test.values.astype('int')))

    ## Test the model & return calculate mean square error
    predictions = knn.predict(X_test.values.reshape(-1, 15))

    np.savetxt("results.csv", predictions, delimiter=",")

    mse = sklearn.metrics.mean_squared_error(y_true=y_test.values, y_pred=predictions)
    print(mse)

print("--------------------- Before balance ------------------------\n")
knn(False)
print("--------------------- After balance ------------------------\n")
knn(True)