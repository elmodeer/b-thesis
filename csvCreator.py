import subprocess
import pandas as pd
import numpy as np
from re import split
import re
from fileCompressor import get_sensor_name


def getValues(argument):
    ints = False
    temp = argument.split(':')
    if len(temp) == 2:
        if temp[0].strip() == 'time_series':
            ints = True
        values = temp[1].strip(' []\n')
        if len(values) > 1:
            if ints:
                return [int(x) for x in values.split(',')[:-1]]
            else:
                return [float(x) for x in values.split(',')[:-1]]
        else:
            return []
    else:
        return []


def get_lines_to_read(s_type):
    # structure is unix timeStamp + time offsets + (sensor components * 2) cause we add std-dev for each component
    switcher = {
        'sg2_acc': 7,
        'sg2_hrt': 9,
        'sg2_gyr': 7,
        'sg2_ple': 3,
        'sg2_ped': 17,
        'sg2_bar': 9,
        # exception: just the sensor components
        'sg2_gps': 12
    }
    return switcher.get(s_type, -1)


def merge(df_collection, prefix):
    # merge with the biggest df
    df_lengths = []
    for i in df_collection:
        df_lengths.append(len(df_collection[i].index))

    biggest_index = df_lengths.index(max(df_lengths))
    df = df_collection[biggest_index]
    complete_df = pd.DataFrame(columns=['time', prefix + '_' + 'accX', 'accX_std',
                                                prefix + '_' + 'accY', 'accY_std',
                                                prefix + '_' + 'accZ', 'accZ_std',
                                                prefix + '_' + 'gyrX', 'gyrX_std',
                                                prefix + '_' + 'gyrY', 'gyrY_std',
                                                prefix + '_' + 'gyrZ', 'gyrZ_std',
                                                prefix + '_' + 'heartR', 'heartR_std',
                                                prefix + '_' + 'h1', 'h1_std',
                                                prefix + '_' + 'h2', 'h2_std',
                                                prefix + '_' + 'h3', 'h3_std',
                                                prefix + '_' + 'steps', 'steps_std',
                                                prefix + '_' + 'WalkingSteps', 'W_St_std',
                                                prefix + '_' + 'RunningSteps', 'RS_std',
                                                prefix + '_' + 'MovingDistance', 'MD_std',
                                                prefix + '_' + 'CaloriesBurned', 'CB_std',
                                                prefix + '_' + 'LastSpeed', 'LS_std',
                                                prefix + '_' + 'LastSteppingFrequency', 'LSF_std',
                                                prefix + '_' + 'LastPedestrianState', 'LPS_std',
                                                prefix + '_' + 'Latitude',
                                                prefix + '_' + 'Longitude',
                                                prefix + '_' + 'Altitude',
                                                prefix + '_' + 'Speed',
                                                prefix + '_' + 'Direction',
                                                prefix + '_' + 'Climb',
                                                prefix + '_' + 'Error',
                                                prefix + '_' + 'MeasuringTime',
                                                prefix + '_' + 'AccuracyLevel',
                                                prefix + '_' + 'HorizontalAccuracy',
                                                prefix + '_' + 'VerticalAccuracy'])

    # remove this df
    del df_collection[biggest_index]

    # start merging
    for i in range(len(df_lengths)):
        df_2 = df_collection[i]
        df_2_length = len(df_2.index)
        for index, row in df.iterrows():
            while index < df_2_length:
                row_df = df.iloc[index]
                row_df_2 = df_2.iloc[index]
                time_diff = row_df['time'] - row_df_2['time']

                if 120 < time_diff < 240:
                    pass
                elif time_diff < 120:
                    pass
                elif time_diff > 240:
                    pass
                else:
                    pass

                # do some shit

    return df


def to_csv(files, prefix, file_path=''):
    df_collection = {}
    index = 0
    for file_name in files:

        # get sensor name
        sensor_name = get_sensor_name(file_name)
        lines_to_read = get_lines_to_read(sensor_name)

        with open(file_path + '/' + file_name, 'rt') as file:
            fileLines = int(
                subprocess.check_output(["wc", "-l", file_path + '/' + file_name]).decode("utf8").split()[0])
            # as every component got its std dev
            lines_per_iteration = lines_to_read
            window = 0
            timeAll = []

            all_1, all_2, all_3, all_4, all_5, all_6, all_7, all_8, all_9, all_10, all_11, all_12 = []
            all_1_std, all_2_std, all_3_std, all_4_std, all_5_std, all_6_std = []
            all_7_std, all_8_std, all_9_std, all_10_std, all_11_std, all_12_std = []

            while window < fileLines:
                file_lines = []
                for i in range(lines_per_iteration):
                    file_lines.append(getValues(file.readline()))

                timeAll.extend(file_lines[0])
                all_1.extend(file_lines[1])
                all_1_std.extend((file_lines[2]))
                if sensor_name == 'sg2_gps':
                    all_2.extend(file_lines[2])
                    all_3.extend(file_lines[3])
                    all_4.extend(file_lines[4])
                    all_5.extend(file_lines[5])
                    all_6.extend(file_lines[6])
                    all_7.extend(file_lines[7])
                    all_8.extend(file_lines[8])
                    all_9.extend(file_lines[9])
                    all_10.extend(file_lines[10])
                    all_11.extend(file_lines[11])
                    all_12.extend(file_lines[12])

                elif sensor_name != 'sg2_ple':
                    all_2.extend(file_lines[3])
                    all_2_std.extend(file_lines[4])
                    all_3.extend(file_lines[5])
                    all_3_std.extend(file_lines[6])
                elif sensor_name in ['sg2_hrt', 'sg2_ped']:
                    all_4.extend(file_lines[7])
                    all_4_std.extend(file_lines[8])
                elif sensor_name == 'sg2_ped':
                    all_5.extend(file_lines[9])
                    all_5_std.extend(file_lines[10])
                    all_6.extend(file_lines[11])
                    all_6_std.extend(file_lines[12])
                    all_7.extend(file_lines[13])
                    all_7_std.extend(file_lines[14])
                    all_8.extend(file_lines[15])
                    all_8_std.extend(file_lines[16])

                # print(window)
                window += lines_per_iteration

            if sensor_name == 'sg2_acc' or sensor_name == 'sg2_gyr':
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_1_std,
                                                   all_2, all_2_std,
                                                   all_3, all_3_std]),
                                  columns=['time',
                                           prefix + '_' + sensor_name + 'X', 'x_std',
                                           prefix + '_' + sensor_name + 'Y', 'y_std',
                                           prefix + '_' + sensor_name + 'Z', 'z_std'])

            elif sensor_name == 'sg2_hrt':
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_1_std,
                                                   all_2, all_2_std,
                                                   all_3, all_3_std,
                                                   all_4, all_4_std]),
                                  columns=['time',
                                           prefix + '_' + sensor_name + '_' + 'HeartRate', 'hr_std',
                                           prefix + '_' + sensor_name + '_' + '2', '2_std',
                                           prefix + '_' + sensor_name + '_' + '3', '3_std',
                                           prefix + '_' + sensor_name + '_' + '4', '4_std'])
            elif sensor_name == 'sg2_ped':
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_1_std,
                                                   all_2, all_2_std,
                                                   all_3, all_3_std,
                                                   all_4, all_4_std,
                                                   all_5, all_5_std,
                                                   all_6, all_6_std,
                                                   all_7, all_7_std,
                                                   all_8, all_8_std]),
                                  columns=['time',
                                           prefix + '_' + sensor_name + '_' + 'steps', 'steps_std',
                                           prefix + '_' + sensor_name + '_' + 'WalkingSteps', 'W_St_std',
                                           prefix + '_' + sensor_name + '_' + 'RunningSteps', 'RS_std',
                                           prefix + '_' + sensor_name + '_' + 'MovingDistance', 'MD_std',
                                           prefix + '_' + sensor_name + '_' + 'CaloriesBurned', 'CB_std',
                                           prefix + '_' + sensor_name + '_' + 'LastSpeed', 'LS_std',
                                           prefix + '_' + sensor_name + '_' + 'LastSteppingFrequency', 'LSF_std',
                                           prefix + '_' + sensor_name + '_' + 'LastPedestrianState', 'LPS_std'])
            elif sensor_name == 'sg2_gps':
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_2,
                                                   all_3, all_4,
                                                   all_5, all_6,
                                                   all_7, all_8,
                                                   all_9, all_10,
                                                   all_11, all_12]),
                                  columns=['time',
                                           prefix + '_' + sensor_name + '_' + 'Latitude',
                                           prefix + '_' + sensor_name + '_' + 'Longitude',
                                           prefix + '_' + sensor_name + '_' + 'Altitude',
                                           prefix + '_' + sensor_name + '_' + 'Speed',
                                           prefix + '_' + sensor_name + '_' + 'Direction',
                                           prefix + '_' + sensor_name + '_' + 'Climb',
                                           prefix + '_' + sensor_name + '_' + 'Error',
                                           prefix + '_' + sensor_name + '_' + 'MeasuringTime',
                                           prefix + '_' + sensor_name + '_' + 'AccuracyLevel',
                                           prefix + '_' + sensor_name + '_' + 'HorizontalAccuracy',
                                           prefix + '_' + sensor_name + '_' + 'VerticalAccuracy'])
            # when sg2_ple
            else:
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_1_std]),
                                  columns=['time',
                                           sensor_name + '_' + 'PlethysmogramGreen', 'ple_std'])

            df.sort_values('time', inplace=True)
            df_collection[index] = df
            index += 1
            file.close()
    # merge data frames:
    all_df = merge(df_collection, prefix)
    print("here")
