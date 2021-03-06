import csv
import sys

import numpy as np
import pandas as pd
from Processing import config


###function to normalize data between zero and one
def normalizer(data, key):
    minimum = float(sys.maxsize)
    maximum = float(-1)

    for value in data:
        try:
            value = float(value)
            if value < minimum:
                minimum = value
            if value > maximum:
                maximum = value
        except ValueError:
            pass

    for i in range(len(data)):
        try:
            data[i] = float(data[i])
            if maximum == minimum: #look at interpolated t007 for an example of why this is the case we could just make a req that all values must be there to keep the row
                data[i] = 1
            else:
                data[i] = (data[i] - minimum) / (maximum - minimum)
        except ValueError:
            if data[i] == key:
                pass

    return data


def main():
    configs = config.Config()

    for file in configs.fileNames:

        original_name = file
        file = configs.localPath + file
        keys = configs.columnNames
        column_data = {}

        for columnName in configs.columnNames:
            column_data[columnName] = []


        ### pre-normalization: removing zeroes, interpolation, and removing missing segments
        df = pd.read_csv(file)

        #remove zeroes from categories in which it doesn't make sense to have a zero value
        df['Heart.Rate'].replace(0, np.nan, inplace=True)
        df['Breathing.Rate'].replace(0, np.nan, inplace=True)

        #interpolate the data linearly to fill in missing values via specified limit, default is forward
        df = df.interpolate(limit = configs.limit)

        #after interpolation, remove rows with missing data in specified amount of columns
        df = df.dropna(thresh = configs.thresh) #at least ten (minus 4) values required in a row to keep the row

        df.to_csv(configs.localPathInterpolated + 'Interpolated_' + original_name, index=False)


        ###process normalization
        dictReader = csv.DictReader(open(configs.localPathInterpolated + 'Interpolated_' + original_name, 'rt'), fieldnames=configs.columnNames,
                                    delimiter=',', quotechar='"')

        for row in dictReader:
            for key in row:
                column_data[key].append(row[key])

        for i in range(4,19):
            column_data[keys[i]] = normalizer(column_data[keys[i]], keys[i])

        with open(configs.localPathNormalized + 'Normalized_' + original_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            writer.writerows(zip(*[column_data[key] for key in keys]))

