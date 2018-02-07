import csv
import config

configs = config.Config()

print(configs.fileNames)

for file in configs.fileNames:
    file = configs.localPath + file

    columns = {}

    for columnName in configs.columnNames:
        columns[columnName] = []

    dictReader = csv.DictReader(open(file, 'rt'), fieldnames=configs.columnNames,
                                delimiter=',', quotechar='"')

    for row in dictReader:
        for key in row:
            columns[key].append(row[key])