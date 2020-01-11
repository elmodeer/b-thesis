from scipy import stats
import subprocess
import numpy as np


def getValues(argument):
    temp = argument.split(':')
    values = temp[1].strip(' []\n')
    if len(values) > 1:
        return [float(x) for x in values.split(',')]
    else:
        return []


def writeListToFile(argument, file, name):
    argument = map(lambda x: str(x) + ',', argument)

    file.write(name)
    file.writelines(argument)
    file.write('\n')


fileName = 'A4acc.txt'
# can loop over files also in future
with open(fileName, 'rt') as infile:
    # bash routine
    fileLines = int(subprocess.check_output(["wc", "-l", fileName]).decode("utf8").split()[0])
    linesPerIteration = 5
    window = 5
    valuesWindow = 3000
    while window < fileLines:
        lines = []
        if window == 2955:
            print('here')
        for i in range(linesPerIteration):
            lines.append(infile.readline())

        unixTime = int(lines[0])
        time = getValues(lines[1])
        accX = getValues(lines[2])
        accY = getValues(lines[3])
        accZ = getValues(lines[4])
        length = len(time)
        loops = int(np.floor(length / valuesWindow))
        if length > valuesWindow:
            rest = length - loops * valuesWindow
            end = valuesWindow
        else:
            rest = length
            end = 0
        start = 0
        if length > 0:
            with open(fileName[:-4] + '_' + 'compressed2.txt', 'at+') as output:
                # process complete windows

                # output.write(lines[0] + '\n')
                # stats.trim_mean(accX[start:end], 0.1)
                timeCompressed = []
                accXCompressed = []
                accYCompressed = []
                accZCompressed = []
                for k in range(loops):
                    # converting microSec to sec
                    timeCompressed.append(np.floor(unixTime + time[int((start + end) / 2)]/1000000))
                    accXCompressed.append(np.round(stats.trim_mean(accX[start:end], 0.1), 2))
                    accYCompressed.append(np.round(stats.trim_mean(accY[start:end], 0.1), 2))
                    accZCompressed.append(np.round(stats.trim_mean(accZ[start:end], 0.1), 2))
                    # update indices
                    if k < loops - 1:
                        start = end
                        end += valuesWindow

                # process rest values
                error = rest / valuesWindow
                if loops > 0:
                    lastElement = timeCompressed[-1]
                else:
                    lastElement = unixTime + time[0] / 1000000
                timeCompressed.append(np.floor(lastElement + 120))
                accXCompressed.append(np.round(error * stats.trim_mean(accX[end:], 0.1), 2))
                accYCompressed.append(np.round(error * stats.trim_mean(accY[end:], 0.1), 2))
                accZCompressed.append(np.round(error * stats.trim_mean(accZ[end:], 0.1), 2))

                # write to file
                # output.write(str(unixTime))
                # output.write('\n')

                writeListToFile(timeCompressed, output, 'time:')
                writeListToFile(accXCompressed, output, 'x:')
                writeListToFile(accYCompressed, output, 'y:')
                writeListToFile(accZCompressed, output, 'z:')
            window += 5
            output.close()
        # pd.DataFrame(accX).plot.hist()
        # average = 0
        # k = 6
        # iir_1 = accX[0]
        # for i in range(3000):
        # average += float(accX[i])
        # iir = k*accX[i] + (1 - k)*iir_1
        # iir_1 = iir

        # print('normal average', average/3000)
        # print('median', (accX[1500] + accX[1499])/2)
        # print('trimmed mean', stats.trim_mean(accX[:3000], 0.1))
