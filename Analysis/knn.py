import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, KFold
from sklearn import metrics, neighbors
import glob
import os
from Processing import config
import numpy as np

# Concatenate all the files from each person into one dataframe
configs = config.Config()
path = configs.localPathAverage
df = pd.concat((pd.read_csv(f) for f in glob.glob(os.path.join(path, '*.csv'))))
df.to_csv("concat.csv", sep=',', index=False)

# Create X - features and y - labels
X = df[['Palm.EDA', 'Heart.Rate', 'Breathing.Rate', 'Perinasal.Perspiration', 'Speed', 'Acceleration', 'Brake', 'Steering', 'LaneOffset', 'Lane.Position', 'Distance', 'Gaze.X.Pos', 'Gaze.Y.Pos', 'Lft.Pupil.Diameter', 'Rt.Pupil.Diameter']]
y = df['Stimulus'].replace([2,3,4,5,6], 1)

# Split features and labels into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Reshape data to appropriate numpy array, values is numpy representation
X_train = X_train.values.reshape(-1,15)
y_train = y_train.values.astype('int')
X_test = X_test.values.reshape(-1,15)
y_test = y_test.values.astype('int')

# Instantiate the model with 50 neighbors.
knn = neighbors.KNeighborsClassifier(n_neighbors=50)

# Fit the model on the training data.
knn.fit(X_train, y_train)

# See how the model performs on the test data.
print("Accuracy: " + str(knn.score(X_test, y_test)))

# Test the model & return calculate mean square error
predictions = knn.predict(X_test)

np.savetxt("results.csv", predictions, delimiter=",")

mse = metrics.mean_squared_error(y_true=y_test, y_pred=predictions)
print("Mean squared error: " + str(mse))

##Should confusion matrix be done on training or test
y_pred = knn.predict(X_train)
cfm = metrics.confusion_matrix(y_train, y_pred)
print(cfm)

##Should cross val score be done on training or test?
print(cross_val_score(knn, X_test, y_test))
