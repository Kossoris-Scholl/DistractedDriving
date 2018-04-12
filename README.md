# DistractedDriving
The National Highway Traffic Safety Administration (NHTSA) reports that 10 percent of fatal crashes in 2015 were classified as distraction-affected crashes. In an effort to make driving safer, we introduce driving stimuli classification to detect driver distraction. We used a simulated driving dataset composed of four different types of stimuli: no distraction, cognitive distraction, emotional distraction, and sensorimotor distraction. Using several machine learning algorithms, we can detect when one of the aforementioned stimuli was applied to a driver, which often leads to distraction of the driver. The classifiers were trained and tested on several response variables during driving: speed, acceleration, brake force, steering and lane position signals, perinasal electrodermal activity (EDA), palm EDA, heart rate, breathing rate, and gaze position. We measured performance of the classifiers using standard accuracy, cross validation, and F1 scores. Results show that machine learning algorithms can effectively detect distracted driving stimuli with a relatively high degree of certainty.

## Setup Instructions
Python 3.5 or higher. 
Dependencies: Pandas, Sklearn

## Processing 
###Unity-Based Normalization
In order to account for differences in each participant's range of each feature, we normalized the data through a standard normalization function. This function normalizes each column of data so that each value is between 0 and 1, inclusive.

normalized data = (data - minimum) / (maximum - minimum)

###Forward Fill Linear Interpolation
This process forward fills missing data in segments of a user specified amount, allowing for more possible data points to be analyzed. We utilized an interpolation function from the pandas library. 

###Data Removal
We removed any zeroes for which it does not make sense to include it in the data. For instance, zero heart rate and breathing rate are not possible, so these were changed to NaNs. Additionally, after interpolation we removed any continuous missing segments of data that were longer than a user specified amount.

###Rolling Mean
In order to dampen large differences over small amounts of time and to reduce outliers in data, we took the mean of each consecutive 10 second interval for each feature. We took a specified rolling window average over the normalized data using pandas rolling mean function.

###Balancing
In order to ensure classifiers were not biased toward one class, we also tested balanced training data where 50% of the input data was labeled distracted and the other 50% was labeled undistracted.​

## Visualization
Visualizer:
This file allows you to compare one feature over time per each run.

## Classification
### K-Nearest Neighbor
### Support Vector Machine
### Random Forest
### Naive Bayes
### Neural Network

## Evaluation
###Accuracy
Baseline accuracy of our data, using a basic percentage of correctly-classified data points

###Mean Squared Error
Mean squared error regression loss between ground truth and estimated target values.

###F1 Scores
Weighted average of precision and recall where its best value is 1 and worst value is 0. Results include Macro, Micro, and Weighted F1 scores.

###Confusion Matrix
Count of true positives, true negatives, false positives, and false negatives.
