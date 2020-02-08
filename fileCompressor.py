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

            unixTime = lines[0]
            time_series = lines[1]
            length = len(time_series)
            #  Compress range to be 2 mins
            loops = 0
            start_index = 0
            end_index = 0

            if length > 1:
                compress_range = int(60000000 / (time_series[1] - time_series[0]))
                if compress_range != 0:
                    loops = int(np.floor(length / compress_range))
                    if length >= compress_range:
                        end_index = compress_range
                # file_name[:-4] -> removes the .txt extension
                with open(output_dir + '/' + file_name[:-4] + '_' + 'compressed.txt', 'a+') as output:
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
                    val1_compressed = []
                    val2_compressed = []
                    val3_compressed = []
                    val4_compressed = []
                    val5_compressed = []
                    val6_compressed = []
                    val7_compressed = []
                    val8_compressed = []
                    val2_std_dev = []
                    val1_std_dev = []
                    val3_std_dev = []
                    val4_std_dev = []
                    val5_std_dev = []
                    val6_std_dev = []
                    val7_std_dev = []
                    val8_std_dev = []

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
                        if sensor_name != 'sg2_ple':
                            val2_compressed.append(np.round(stats.trim_mean(lines[3][start_index:end_index], 0.1), 2))
                            val2_std_dev.append(np.round(np.std(lines[3][start_index:end_index]), 2))

                            val3_compressed.append(np.round(stats.trim_mean(lines[4][start_index:end_index], 0.1), 2))
                            val3_std_dev.append(np.round(np.std(lines[4][start_index:end_index]), 2))
                        if sensor_name in ['sg2_hrt', 'sg2_ped', 'sg2_bar']:
                            val4_compressed.append(np.round(stats.trim_mean(lines[5][start_index:end_index], 0.1), 2))
                            val4_std_dev.append(np.round(np.std(lines[5][start_index:end_index]), 2))
                        if sensor_name == 'sg2_ped':
                            val5_compressed.append(np.round(stats.trim_mean(lines[6][start_index:end_index], 0.1), 2))
                            val5_std_dev.append(np.round(np.std(lines[6][start_index:end_index]), 2))

                            val6_compressed.append(np.round(stats.trim_mean(lines[7][start_index:end_index], 0.1), 2))
                            val6_std_dev.append(np.round(np.std(lines[7][start_index:end_index]), 2))

                            val7_compressed.append(np.round(stats.trim_mean(lines[8][start_index:end_index], 0.1), 2))
                            val7_std_dev.append(np.round(np.std(lines[8][start_index:end_index]), 2))

                            val8_compressed.append(np.round(stats.trim_mean(lines[9][start_index:end_index], 0.1), 2))
                            val8_std_dev.append(np.round(np.std(lines[9][start_index:end_index]), 2))

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
                        time_element = int(lastElement + 120)
                        if match_unix_stamp(time_element):
                            time_series_compressed.append(time_element)
                            val1_compressed.append(np.round(stats.trim_mean(lines[2][end_index:], 0.1), 2))
                            val1_std_dev.append(np.round(np.std(lines[2][end_index:]), 2))
                            if math.isnan(val1_compressed[-1]) or math.isnan(val1_std_dev[-1]):
                                print("nan")
                            if sensor_name != 'sg2_ple':
                                val2_compressed.append(np.round(stats.trim_mean(lines[3][end_index:], 0.1), 2))
                                val2_std_dev.append(np.round(np.std(lines[3][end_index:]), 2))

                                val3_compressed.append(np.round(stats.trim_mean(lines[4][end_index:], 0.1), 2))
                                val3_std_dev.append(np.round(np.std(lines[4][end_index:]), 2))
                            if sensor_name in ['sg2_hrt', 'sg2_ped', 'sg2_bar']:
                                val4_compressed.append(np.round(stats.trim_mean(lines[5][end_index:], 0.1), 2))
                                val4_std_dev.append(np.round(np.std(lines[5][end_index:]), 2))

                            if sensor_name == 'sg2_ped':
                                val5_compressed.append(np.round(stats.trim_mean(lines[6][end_index:], 0.1), 2))
                                val5_std_dev.append(np.round(np.std(lines[6][end_index:]), 2))

                                val6_compressed.append(np.round(stats.trim_mean(lines[7][end_index:], 0.1), 2))
                                val6_std_dev.append(np.round(np.std(lines[7][end_index:]), 2))

                                val7_compressed.append(np.round(stats.trim_mean(lines[8][end_index:], 0.1), 2))
                                val7_std_dev.append(np.round(np.std(lines[8][end_index:]), 2))

                                val8_compressed.append(np.round(stats.trim_mean(lines[9][end_index:], 0.1), 2))
                                val8_std_dev.append(np.round(np.std(lines[9][end_index:]), 2))
                    # only write when there is data in the lists
                    if len(time_series_compressed) != 0:
                        writeListToFile(time_series_compressed, output, 'time_series:')
                        writeListToFile(val1_compressed, output, '1:')
                        writeListToFile(val1_std_dev, output, 'val1_std_dev:')

                        if sensor_name != 'sg2_ple':
                            writeListToFile(val2_compressed, output, '2:')
                            writeListToFile(val2_std_dev, output, 'val2_std_dev:')

                            writeListToFile(val3_compressed, output, '3:')
                            writeListToFile(val3_std_dev, output, 'val3_std_dev:')
                        if sensor_name in ['sg2_hrt', 'sg2_ped', 'sg2_bar']:
                            writeListToFile(val4_compressed, output, '4:')
                            writeListToFile(val4_std_dev, output, 'val4_std_dev:')

                        if sensor_name == 'sg2_ped':
                            writeListToFile(val5_compressed, output, '5:')
                            writeListToFile(val5_std_dev, output, 'val5_std_dev:')

                            writeListToFile(val6_compressed, output, '6:')
                            writeListToFile(val6_std_dev, output, 'val6_std_dev:')

                            writeListToFile(val7_compressed, output, '7:')
                            writeListToFile(val7_std_dev, output, 'val7_std_dev:')

                            writeListToFile(val8_compressed, output, '8:')
                            writeListToFile(val8_std_dev, output, 'val8_std_dev:')
                output.close()
            window += components
        infile.close()
        print(str(window) + ' read from ' + str(file_lines))
        print("compression finished for file " + file_name)
