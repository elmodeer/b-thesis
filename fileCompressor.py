import matplotlib
from re import split
from scipy import stats
import subprocess
import math
import numpy as np
from numpy import fft
from matplotlib import pyplot as plt


# %matplotlib inline

def getValues(argument, ints=False):
    temp = argument.split(':')
    values = temp[1].strip(' []\n')
    if len(values) > 1:
        if ints:
            return [int(x) for x in values.split(',')]
        else:
            return [float(x) for x in values.split(',')]
    else:
        return []


def writeListToFile(argument, file, name):
    argument = map(lambda x: str(x) + ',', argument)

    file.write(name)
    file.writelines(argument)
    file.write('\n')


def get_sensor_name(file_name):
    sensor_name_length = len('sg2_xxx')
    start_index = file_name.find('sg2')
    return file_name[start_index:sensor_name_length]


def getComponents(s_type):
    # structure is unix timeStamp + time offsets + sensor components
    switcher = {
        'sg2_acc': 5,
        'sg2_hrt': 6,
        'sg2_gyr': 5,
        'sg2_ple': 3,
        'sg2_ped': 10,
        'sg2_bar': 6,
        'sg2_gps': 13

    }
    return switcher.get(s_type, -1)


def get_lines(in_file,components):
    lines = []
    for i in range(components):
        # parsing unix time stamp
        if i == 0:
            lines.append(int(in_file.readline()))
            continue
        # parsing time offsets
        if i == 1:
            lines.append(getValues(in_file.readline(), ints=True))
            continue
        # parsing normal sensor values
        lines.append(getValues(in_file.readline()))
    return lines


# def compress_gps(file_name, output_dir='', file_path=''):
#     sensor_name = get_sensor_name(file_name)
#     components = 13
#
#     with open(file_path + '/' + file_name, 'rt') as in_file:
#         # bash routine
#         file_lines = int(subprocess.check_output(["wc", "-l", file_path + '/' + file_name]).decode("utf8").split()[0])
#         window = components
#         while window < file_lines:
#             lines = get_lines(in_file, components)
#             unix_time = lines[0]
#             time_series = lines[1]
#             with open(output_dir + '/' + file_name[:-4] + '_' + 'compressed.txt', 'at+') as output:


def compress(file_name, output_dir='', file_path=''):
    """
    compress the data with some way and also generates the std dev of the compressed range
    :param file_name: files name to open
    :param output_dir: where to put the files
    :param file_path: where the file is
    :return: void
    """

    sensor_name = get_sensor_name(file_name)
    components = getComponents(sensor_name)

    with open(file_path + '/' + file_name, 'rt') as infile:
        # bash routine
        file_lines = int(subprocess.check_output(["wc", "-l", file_path + '/' + file_name]).decode("utf8").split()[0])
        window = components
        # values_window = 3000
        while window < file_lines:
            lines = get_lines(infile, components)

            unixTime = lines[0]
            time_series = lines[1]
            length = len(time_series)
            #  Compress range to be 2 mins
            loops = 0
            start_index = 0
            end_index = 0

            if length > 1:
                compress_range = int(120000000 / (time_series[1] - time_series[0]))
                if compress_range != 0:
                    loops = int(np.floor(length / compress_range))
                    if length >= compress_range:
                        end_index = compress_range
                # file_name[:-4] -> removes the .txt extension
                with open(output_dir + '/' + file_name[:-4] + '_' + 'compressed.txt', 'at+') as output:
                    # process complete windows

                    # output.write(lines[0] + '\n')
                    # stats.trim_mean(valueX[start_index:end_index], 0.1)
                    # fs = 0.25 * 10 ** 6
                    # pyplot.plot(valueX[:3000])
                    # pyplot.show()
                    # ls = np.linspace(0, fs, 3000)
                    # fft_res = fft.rfft(valueX[:3000])
                    # pyplot.plot(ls, np.abs(fft_res))

                    # plt.plot(ls, valueX[:3000], label='acc X')
                    # plt.plot(ls, value2[:3000], label='acc y')
                    # plt.plot(ls, valueZ[:3000], label='acc Z')
                    # plt.legend_index(framealpha=1, frameon=True)

                    # plt.show()
                    #
                    # print('asdf')
                    time_series_compressed = []
                    value1_compressed = []
                    value1_std_Dev = []

                    value2_compressed = []
                    value2_std_Dev = []

                    value3_compressed = []
                    value3_std_Dev = []

                    value4_compressed = []
                    value4_std_Dev = []

                    value5_compressed = []
                    value5_std_Dev = []

                    value6_compressed = []
                    value6_std_Dev = []

                    value7_compressed = []
                    value7_std_Dev = []

                    value8_compressed = []
                    value8_std_Dev = []

                    for k in range(loops):
                        # converting microSec to sec
                        # if components == 'three':
                        if (end_index - start_index) != compress_range:
                            print('wrong indices are being evaluated')
                        time_series_compressed.append(
                            int(unixTime + time_series[int((start_index + end_index) / 2)] / 1000000))

                        value1_compressed.append(np.round(stats.trim_mean(lines[2][start_index:end_index], 0.1), 2))
                        value1_std_Dev.append(np.round(np.std(lines[2][start_index:end_index]), 2))
                        if math.isnan(value1_compressed[-1]) or math.isnan(value1_std_Dev[-1]):
                            print("nan")
                        if sensor_name != 'sg2_ple':
                            value2_compressed.append(np.round(stats.trim_mean(lines[3][start_index:end_index], 0.1), 2))
                            value2_std_Dev.append(np.round(np.std(lines[3][start_index:end_index]), 2))

                            value3_compressed.append(np.round(stats.trim_mean(lines[4][start_index:end_index], 0.1), 2))
                            value3_std_Dev.append(np.round(np.std(lines[4][start_index:end_index]), 2))
                        if sensor_name == 'sg2_hrt' or sensor_name == 'sg2_ped':
                            value4_compressed.append(np.round(stats.trim_mean(lines[5][start_index:end_index], 0.1), 2))
                            value4_std_Dev.append(np.round(np.std(lines[5][start_index:end_index]), 2))
                        if sensor_name == 'sg2_ped':
                            value5_compressed.append(np.round(stats.trim_mean(lines[6][start_index:end_index], 0.1), 2))
                            value5_std_Dev.append(np.round(np.std(lines[6][start_index:end_index]), 2))

                            value6_compressed.append(np.round(stats.trim_mean(lines[7][start_index:end_index], 0.1), 2))
                            value6_std_Dev.append(np.round(np.std(lines[7][start_index:end_index]), 2))

                            value7_compressed.append(np.round(stats.trim_mean(lines[8][start_index:end_index], 0.1), 2))
                            value7_std_Dev.append(np.round(np.std(lines[8][start_index:end_index]), 2))

                            value8_compressed.append(np.round(stats.trim_mean(lines[9][start_index:end_index], 0.1), 2))
                            value8_std_Dev.append(np.round(np.std(lines[9][start_index:end_index]), 2))

                        # update indices
                        if k < loops - 1:
                            start_index = end_index
                            end_index += compress_range

                    # process rest values
                    if loops > 0:
                        lastElement = time_series_compressed[-1]
                    else:
                        lastElement = unixTime + time_series[0] / 1000000
                    if length != end_index:
                        time_series_compressed.append(int(lastElement + 120))
                        value1_compressed.append(np.round(stats.trim_mean(lines[2][end_index:], 0.1), 2))
                        value1_std_Dev.append(np.round(np.std(lines[2][end_index:]), 2))
                        if math.isnan(value1_compressed[-1]) or math.isnan(value1_std_Dev[-1]):
                            print("nan")
                        if sensor_name != 'sg2_ple':
                            value2_compressed.append(np.round(stats.trim_mean(lines[3][end_index:], 0.1), 2))
                            value2_std_Dev.append(np.round(np.std(lines[3][end_index:]), 2))

                            value3_compressed.append(np.round(stats.trim_mean(lines[4][end_index:], 0.1), 2))
                            value3_std_Dev.append(np.round(np.std(lines[4][end_index:]), 2))
                        if sensor_name == 'sg2_hrt' or sensor_name == 'sg2_ped':
                            value4_compressed.append(np.round(stats.trim_mean(lines[5][end_index:], 0.1), 2))
                            value4_std_Dev.append(np.round(np.std(lines[5][end_index:]), 2))

                        if sensor_name == 'sg2_ped':
                            value5_compressed.append(np.round(stats.trim_mean(lines[6][end_index:], 0.1), 2))
                            value5_std_Dev.append(np.round(np.std(lines[6][end_index:]), 2))

                            value6_compressed.append(np.round(stats.trim_mean(lines[7][end_index:], 0.1), 2))
                            value6_std_Dev.append(np.round(np.std(lines[7][end_index:]), 2))

                            value7_compressed.append(np.round(stats.trim_mean(lines[8][end_index:], 0.1), 2))
                            value7_std_Dev.append(np.round(np.std(lines[8][end_index:]), 2))

                            value8_compressed.append(np.round(stats.trim_mean(lines[9][end_index:], 0.1), 2))
                            value8_std_Dev.append(np.round(np.std(lines[9][end_index:]), 2))

                    writeListToFile(time_series_compressed, output, 'time_series:')
                    writeListToFile(value1_compressed, output, '1:')
                    writeListToFile(value1_std_Dev, output, 'value1_std_Dev:')

                    if components == 5 or components == 6 or components == 10:
                        writeListToFile(value2_compressed, output, '2:')
                        writeListToFile(value2_std_Dev, output, 'value2_std_Dev:')

                        writeListToFile(value3_compressed, output, '3:')
                        writeListToFile(value3_std_Dev, output, 'value3_std_Dev:')
                    if components == 6 or components == 10:
                        writeListToFile(value4_compressed, output, '4:')
                        writeListToFile(value4_std_Dev, output, 'value4_std_Dev:')

                    if components == 10:
                        writeListToFile(value5_compressed, output, '5:')
                        writeListToFile(value5_std_Dev, output, 'value5_std_Dev:')

                        writeListToFile(value6_compressed, output, '6:')
                        writeListToFile(value6_std_Dev, output, 'value6_std_Dev:')

                        writeListToFile(value7_compressed, output, '7:')
                        writeListToFile(value7_std_Dev, output, 'value7_std_Dev:')

                        writeListToFile(value8_compressed, output, '8:')
                        writeListToFile(value8_std_Dev, output, 'value8_std_Dev:')
                output.close()
            window += components
