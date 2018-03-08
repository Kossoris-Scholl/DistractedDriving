import pandas as pd
from sklearn import metrics, neighbors

from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
import sklearn
import glob
import os
from Processing import config
import numpy as np


# Concatenate all the files from each person into one dataframe
configs = config.Config()
path = configs.localPathAverage
df = pd.concat((pd.read_csv(f) for f in glob.glob(os.path.join(path, '*.csv'))))
df = df.fillna(method='ffill')

X = df['Breathing.Rate']
y = df['Stimulus']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

X_train = X_train.drop('Breathing.Rate').values.reshape(-1,1)
y_train = y_train.values

## Instantiate the model with 5 neighbors.
knn = sklearn.neighbors.KNeighborsClassifier(n_neighbors=50)

## Fit the model on the training data.
knn.fit(X_train, y_train)

## See how the model performs on the test data.
print(knn.score(X_test.values.reshape(-1,1), y_test.values))

## Test the model & return calculate mean square error
predictions = knn.predict(X_test.values.reshape(-1,   1))

np.savetxt("results.csv", predictions, delimiter=",")

mse = sklearn.metrics.mean_squared_error(y_true=X_test.values.reshape(-1,1), y_pred=predictions)
print(mse)
