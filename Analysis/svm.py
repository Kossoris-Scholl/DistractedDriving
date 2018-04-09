import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, KFold
from sklearn import metrics
from sklearn.svm import SVC
import glob
import os
from Processing import config
import numpy as np


def svm(balanced=False):
    if balanced:
        # Group by Stimulus column so we can access count of each type of stimulus (0 and 1)
        g = df.groupby('Stimulus')

        # Get equal count of each type of stimulus (0 or 1) in new dataframe g
        g = g.apply(lambda x: x.sample(g.size().min()).reset_index(drop=True))

        # Create X - features and y - labels
        X = g[['Palm.EDA', 'Heart.Rate', 'Breathing.Rate', 'Perinasal.Perspiration', 'Speed', 'Acceleration', 'Brake',
               'Steering', 'LaneOffset', 'Lane.Position', 'Distance', 'Gaze.X.Pos', 'Gaze.Y.Pos', 'Lft.Pupil.Diameter',
               'Rt.Pupil.Diameter']]
        y = g['Stimulus']
    else:
        # Create X - features and y - labels
        X = df[['Palm.EDA', 'Heart.Rate', 'Breathing.Rate', 'Perinasal.Perspiration', 'Speed', 'Acceleration', 'Brake',
                'Steering', 'LaneOffset', 'Lane.Position', 'Distance', 'Gaze.X.Pos', 'Gaze.Y.Pos', 'Lft.Pupil.Diameter',
                'Rt.Pupil.Diameter']]
        y = df['Stimulus']

    # Split features and labels into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    # Reshape data to appropriate numpy array, values is numpy representation
    X_train = X_train.values.reshape(-1, 15)
    y_train = y_train.values.astype('int')
    X_test = X_test.values.reshape(-1, 15)
    y_test = y_test.values.astype('int')

    svc = SVC(kernel='rbf', C=50)

    svc.fit(X_train, y_train)

    results = {}

    # See how the model performs on the test data.
    results['accuracy'] = svc.score(X_test, y_test)
    print("Accuracy: " + str(results['accuracy']))

    # Test the model & return calculate mean square error
    predictions = svc.predict(X_test)

    if balanced:
        np.savetxt("svmresults-balanced.csv", predictions, delimiter=",")
    else:
        np.savetxt("svmresults.csv", predictions, delimiter=",")

    results['mse'] = metrics.mean_squared_error(y_true=y_test, y_pred=predictions)
    print("Mean squared error: " + str(results['mse']))

    y_pred = svc.predict(X_test)

    print("Confusion Matrix:")
    results['cfm'] = metrics.confusion_matrix(y_test, y_pred)
    print(results['cfm'])
    print("-----------------")

    results['cross_val_score'] = cross_val_score(svc, X_test, y_test)
    print("Cross Validation Scores: " + str(results['cross_val_score']))

    results['f1_macro'] = metrics.f1_score(y_test, y_pred, average='macro')
    print("F1 Score: Macro")
    print(results['f1_macro'])
    results['f1_micro'] = metrics.f1_score(y_test, y_pred, average='micro')
    print("F1 Score: Micro")
    print(results['f1_micro'])
    results['f1_weighted'] = metrics.f1_score(y_test, y_pred, average='weighted')
    print("F1 Score: Weighted")
    print(results['f1_weighted'])
    results['f1_none'] = metrics.f1_score(y_test, y_pred, average=None)
    print("F1 Score: None")
    print(results['f1_none'])

    return results


# Concatenate all the files from each person into one dataframe
configs = config.Config()
path = configs.localPathAverage
df = pd.concat((pd.read_csv(f) for f in glob.glob(os.path.join(path, '*.csv'))))

# Binary classification
df['Stimulus'] = df['Stimulus'].replace([2, 3, 4, 5, 6], 1)

def main():
    print("--------------------- SVM Results ------------------------\n")
    print("--------------------- Before balance ------------------------\n")
    unbalanced = svm(False)
    print("\n--------------------- After balance ------------------------\n")
    balanced = svm(True)
    return unbalanced, balanced