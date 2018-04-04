# DistractedDriving
The National Highway Traffic Safety Administration (NHTSA) reports that 10 percent of fatal crashes in 2015 were classified as distraction-affected crashes. In an effort to make driving safer, we introduce driving stimuli classification to detect driver distraction. We used a simulated driving dataset composed of four different types of stimuli: no distraction, cognitive distraction, emotional distraction, and sensorimotor distraction. Using several machine learning algorithms, we can detect when one of the aforementioned stimuli was applied to a driver, which often leads to distraction of the driver. The classifiers were trained and tested on several response variables during driving: speed, acceleration, brake force, steering and lane position signals, perinasal electrodermal activity (EDA), palm EDA, heart rate, breathing rate, and gaze position. We measured performance of the classifiers using standard accuracy, cross validation, and F1 scores. Results show that machine learning algorithms can effectively detect distracted driving stimuli with a relatively high degree of certainty.

# Setup Instructions
Python 3.5 or higher. 
Dependencies: Pandas, Sklearn

## Processing 
Normalizer:
This file does 3 things:
1) Data Removal. We r1emove any zeroes for which it does not make sense to include it in the data. For instance, zero heart rate and breathing rate are not possible, so these were changed to NaNs.
2) Linear interpolation. This utilizes the pandas interpolation function to forward-fill gaps in data. This is a user-specified amount.
3) Normalization. This function normalizes each column of data so that each value is between 0 and 1, inclusive. We used the function: normalized data = (data - minimum) / (maximum - minimum)

Rolling Mean:
This file has one main function: take a specified rolling window average over the normalized data using pandas rolling mean function.

## Visualization
Visualizer:
This file allows you to compare one feature over time per each run.

## Classification
### K-Nearest Neighbor
### Support Vector Machine
### Random Forest
### Naive Bayes
### Neural Network
