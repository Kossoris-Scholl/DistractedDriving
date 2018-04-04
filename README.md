# DistractedDriving
Distracted driving event detection.

##Processing

Normalizer:
This file does 3 things:
1) Data Removal. We r1emove any zeroes for which it does not make sense to include it in the data. For instance, zero heart rate and breathing rate are not possible, so these were changed to NaNs.
2) Linear interpolation. This utilizes the pandas interpolation function to forward-fill gaps in data. This is a user-specified amount.
3) Normalization. This function normalizes each column of data so that each value is between 0 and 1, inclusive. We used the function: normalized data = (data - minimum) / (maximum - minimum)

Rolling Mean:
This file has one main function: take a specified rolling window average over the normalized data using pandas rolling mean function.

Visualizer:
This file allows you to compare one feature over time per each run.



