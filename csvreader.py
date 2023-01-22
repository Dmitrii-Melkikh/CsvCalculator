import sys
import time
import re
import pandas as pd

def splitCell(s: str):
    index = -1
    for i in range(len(s)):
        if s[i].isdigit():
            index = i
            break
    return s[:index], s[index:]

print(sys.argv[0])
try:
    df = pd.read_csv(sys.argv[1])
except():
    print('Неправильный формат таблицы или таблицы не существует')
    sys.exit(0)
df = df.rename(columns={df.columns[0]: "RowNum"})


for rowIndex, row in df.iterrows():
    for columnIndex, value in row.items():
        cell = str(value)
        if cell[0] == '=':
            cell = cell[1:]
            cells = re.split('(\W)', cell)
            rows = []
            colums = []

            firstArgColumn, firstArgRow = splitCell(cells[0])
            secondArgColumn, secondArgRow = splitCell(cells[2])
            try:
                k = df.loc[df['RowNum'] == int(firstArgRow), firstArgColumn].iloc[0]
                k1 = df.loc[df['RowNum'] == int(secondArgRow), secondArgColumn].iloc[0]
                result = str(k) + cells[1] + str(k1)
                try:
                    result = eval(result)

                    df.at[rowIndex, columnIndex] = result
                except(ZeroDivisionError):
                    print('В строке \'=' + ''.join(cells) + '\' попытка деления на ноль')
                    sys.exit(0)
            except():
                print('В таблице присутствуют неправильные адреса ячеек')
                sys.exit(0)



s=''
for i in df.columns.values.tolist():
    if i != 'RowNum':
        s += ',' + i
print(s)
for rowIndex, row in df.iterrows(): #iterate over rows
    listOfValues = []
    for columnIndex, value in row.items():
        listOfValues.append(str(value))
    print(','.join(listOfValues))

