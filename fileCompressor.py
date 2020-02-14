import matplotlib
from scipy import stats
import subprocess
import math
import numpy as np
from fluffUtil import get_sensor_name, get_lines, writeListToFile, match_unix_stamp, get_components
from numpy import fft
from matplotlib import pyplot as plt


# %matplotlib inline


def compress(file_name, output_dir='', file_path=''):
    """
    compress the data with some way and also generates the std dev of the compressed range
    :param file_name: files name to open
    :param output_dir: where to put the files
    :param file_path: where the file is
    :return: void
    """

    sensor_name = get_sensor_name(file_name)
    components = get_components(sensor_name)

    with open(file_path + '/' + file_name, 'rt') as infile:
        # bash routine
        file_lines = int(subprocess.check_output(["wc", "-l", file_path + '/' + file_name]).decode("utf8").split()[0])
        window = components
        # values_window = 3000
        while window < file_lines:
            lines = get_lines(infile, components)
            if len(lines) == 0:
                window += components
                continue
            unixTime = lines[0]
            time_series = lines[1]
            length = len(time_series)
            #  Compress range to be 2 mins
            loops = 0
            start_index = 0
            end_index = 0

            if length > 1:
                if (time_series[1] - time_series[0]) != 0:
                    compress_range = int(60000000 / (time_series[1] - time_series[0]))
                else:
                    print('corrupt entry')
                    continue
                if compress_range != 0:
                    loops = int(np.floor(length / compress_range))
                    if length >= compress_range:
                        end_index = compress_range
                # file_name[:-4] -> removes the .txt extension
                with open(output_dir + '/' + file_name[:-4] + '_' + 'compressed.txt', 'a+') as output:

                    time_series_compressed = []
                    val1_compressed = []
                    val2_compressed = []
                    val3_compressed = []
                    val4_compressed = []
                    val2_std_dev = []
                    val1_std_dev = []
                    val3_std_dev = []
                    val4_std_dev = []

                    for k in range(loops):
                        # converting microSec to sec
                        # if components == 'three':
                        if (end_index - start_index) != compress_range:
                            print('wrong indices are being evaluated')

                        time_element = int(unixTime + time_series[int((start_index + end_index) / 2)] / 1000000)
                        if match_unix_stamp(time_element):
                            time_series_compressed.append(time_element)
                        else:
                            # this entry is corrupt
                            continue

                        val1_compressed.append(np.round(stats.trim_mean(lines[2][start_index:end_index], 0.1), 2))
                        val1_std_dev.append(np.round(np.std(lines[2][start_index:end_index]), 2))
                        if math.isnan(val1_compressed[-1]) or math.isnan(val1_std_dev[-1]):
                            print("nan")
                        if sensor_name in ['sg2_gyr', 'sg2_bar', 'sg2_acc', 'sg2_ped']:
                            val2_compressed.append(np.round(stats.trim_mean(lines[3][start_index:end_index], 0.1), 2))
                            val2_std_dev.append(np.round(np.std(lines[3][start_index:end_index]), 2))

                            val3_compressed.append(np.round(stats.trim_mean(lines[4][start_index:end_index], 0.1), 2))
                            val3_std_dev.append(np.round(np.std(lines[4][start_index:end_index]), 2))
                        if sensor_name in ['sg2_bar', 'sg2_ped', 'sg2_bar']:
                            val4_compressed.append(np.round(stats.trim_mean(lines[5][start_index:end_index], 0.1), 2))
                            val4_std_dev.append(np.round(np.std(lines[5][start_index:end_index]), 2))

                        # update indices
                        if k < loops - 1:
                            start_index = end_index
                            end_index += compress_range

                    # process rest values
                    if loops > 0 and len(time_series_compressed) != 0 :
                        lastElement = time_series_compressed[-1]
                    else:
                        lastElement = unixTime + time_series[0] / 1000000
                    if length != end_index:
                        time_element = int(lastElement + 120)
                        if match_unix_stamp(time_element):
                            time_series_compressed.append(time_element)
                            val1_compressed.append(np.round(stats.trim_mean(lines[2][end_index:], 0.1), 2))
                            val1_std_dev.append(np.round(np.std(lines[2][end_index:]), 2))
                            if math.isnan(val1_compressed[-1]) or math.isnan(val1_std_dev[-1]):
                                print("nan")
                            if sensor_name in ['sg2_gyr', 'sg2_bar', 'sg2_acc', 'sg2_ped']:
                                val2_compressed.append(np.round(stats.trim_mean(lines[3][end_index:], 0.1), 2))
                                val2_std_dev.append(np.round(np.std(lines[3][end_index:]), 2))

                                val3_compressed.append(np.round(stats.trim_mean(lines[4][end_index:], 0.1), 2))
                                val3_std_dev.append(np.round(np.std(lines[4][end_index:]), 2))
                            if sensor_name in ['sg2_bar', 'sg2_ped', 'sg2_bar']:
                                val4_compressed.append(np.round(stats.trim_mean(lines[5][end_index:], 0.1), 2))
                                val4_std_dev.append(np.round(np.std(lines[5][end_index:]), 2))

                    # only write when there is data in the lists
                    if len(time_series_compressed) != 0:
                        writeListToFile(time_series_compressed, output, 'time_series:')
                        writeListToFile(val1_compressed, output, '1:')
                        writeListToFile(val1_std_dev, output, 'val1_std_dev:')

                        if sensor_name in ['sg2_gyr', 'sg2_bar', 'sg2_acc', 'sg2_ped']:
                            writeListToFile(val2_compressed, output, '2:')
                            writeListToFile(val2_std_dev, output, 'val2_std_dev:')

                            writeListToFile(val3_compressed, output, '3:')
                            writeListToFile(val3_std_dev, output, 'val3_std_dev:')
                        if sensor_name in ['sg2_bar', 'sg2_ped', 'sg2_bar']:
                            writeListToFile(val4_compressed, output, '4:')
                            writeListToFile(val4_std_dev, output, 'val4_std_dev:')

                output.close()
            window += components
        infile.close()
        print(str(window) + ' read from ' + str(file_lines))
        print("compression finished for file " + file_name)
