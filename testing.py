import csv
stonkList = []

with open('TSX.txt', 'r') as file_in:
    file_in.readline() #Skip the first line
    for line in file_in:
        symbol = line.split('\t')[0]
        stonkList.append(symbol)

#     dictReader = csv.DictReader(file_in)
#     for line in dictReader:
#         print(line)
# #         symbol = line.split(' ')[0]
#         stonkList.append(symbol)
print(stonkList)