import subprocess
import pandas as pd
import numpy as np
import openpyxl

def getValues(argument):
    temp = argument.split(':')
    values = temp[1].strip('\n')
    if len(values) > 1:
        return [float(x) for x in values.split(',')[:-1]]
    else:
        return []


fileName = 'A4acc_compressed2.txt'
with open(fileName, 'rt') as file:
    fileLines = int(subprocess.check_output(["wc", "-l", fileName]).decode("utf8").split()[0])
    linesPerIteration = 4
    window = 0
    timeAll = []
    accXAll = []
    accYAll = []
    accZAll = []
    print(fileLines)
    while window < fileLines:
        lines = []
        for i in range(linesPerIteration):
            lines.append(file.readline())
        time = getValues(lines[0])
        accX = getValues(lines[1])
        accY = getValues(lines[2])
        accZ = getValues(lines[3])
        # if window == 0:
        #     df = pd.DataFrame(np.column_stack([time, accX, accY, accZ]),
        #                       columns=['time', 'x', 'y', 'z'])
        #     df.to_csv('A4accAll_a.csv', mode='a', index=False)
        # else:
        #     df = pd.DataFrame(np.column_stack([time, accX, accY, accZ]))
        #     df.to_csv('A4accAll_a.csv', mode='a', index=False)
        timeAll.extend(time)
        accXAll.extend(accX)
        accYAll.extend(accY)
        accZAll.extend(accZ)
        # print(window)
        window += linesPerIteration
    df = pd.DataFrame(np.column_stack([timeAll, accXAll, accYAll, accZAll]),
                      columns=['time', 'x', 'y', 'z'])
    df.sort_values('time', inplace=True)
    # df.to_excel('A4accAll.xlsx')
    df.to_csv('All.csv', index=False)
    file.close()
