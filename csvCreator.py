import subprocess
import pandas as pd
import numpy as np
# from fileCompressor import getValues
from re import split


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
    # structure is unix timeStamp + time offsets + sensor components
    switcher = {
        'sg2_acc': 7,
        'sg2_hrt': 9,
        'sg2_gyr': 7,
        'sg2_ple': 3,
        'sg2_ped': 17,
        'sg2_bar': 9,
        'sg2_gps': 13
    }
    return switcher.get(s_type, -1)


def merge_matching_df(df_matching, df_2, df_rest):
    print('sadf')


def merge(df_collection):
    # merge with the biggest df
    df_lengths = []
    for i in df_collection:
        df_lengths.append(len(df_collection[i].index))

    biggest_index = df_lengths.index(max(df_lengths))
    df = df_collection[biggest_index]

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
                # do some shit

    return df


def to_csv(files, prefix, file_path=''):
    df_collection = {}
    index = 0
    for file_name in files:
        x = split('_', file_name)

        # get sensor name
        sensor_name = x[1] + '_' + x[2]
        lines_to_read = get_lines_to_read(sensor_name)

        with open(file_path + '/' + file_name, 'rt') as file:
            fileLines = int(subprocess.check_output(["wc", "-l", file_path + '/' + file_name]).decode("utf8").split()[0])
            # as every component got its std dev
            lines_per_iteration = lines_to_read
            window = 0
            timeAll = []

            all_1 = []
            all_1_stdev = []

            all_2 = []
            all_2_stdev = []

            all_3 = []
            all_3_stdev = []

            all_4 = []
            all_4_stdev = []

            all_5 = []
            all_5_stdev = []

            all_6 = []
            all_6_stdev = []

            all_7 = []
            all_7_stdev = []

            all_8 = []
            all_8_stdev = []

            # print(file_name + ', ' + str(fil))
            while window < fileLines:
                file_lines = []
                for i in range(lines_per_iteration):
                    file_lines.append(getValues(file.readline()))

                timeAll.extend(file_lines[0])
                all_1.extend(file_lines[1])
                all_1_stdev.extend((file_lines[2]))
                # if len(all_1) != len(all_1_stdev):
                #     print("asdfas")
                if sensor_name == 'sg2_acc' or sensor_name == 'sg2_hrt' or sensor_name == 'sg2_ped':
                    all_2.extend(file_lines[3])
                    all_2_stdev.extend(file_lines[4])
                    all_3.extend(file_lines[5])
                    all_3_stdev.extend(file_lines[6])
                if sensor_name == 'sg2_hrt' or sensor_name == 'sg2_ped':
                    all_4.extend(file_lines[7])
                    all_4_stdev.extend(file_lines[8])
                if sensor_name == 'sg2_ped':
                    all_5.extend(file_lines[9])
                    all_5_stdev.extend(file_lines[10])
                    all_6.extend(file_lines[11])
                    all_6_stdev.extend(file_lines[12])
                    all_7.extend(file_lines[13])
                    all_7_stdev.extend(file_lines[14])
                    all_8.extend(file_lines[15])
                    all_8_stdev.extend(file_lines[16])
                # print(window)
                window += lines_per_iteration

            if sensor_name == 'sg2_acc' or sensor_name == 'sg2_gyr':
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_1_stdev,
                                                   all_2, all_2_stdev,
                                                   all_3, all_3_stdev]),
                                  columns=['time',
                                           prefix + '_' + sensor_name + '_' + '1', '1_std',
                                           prefix + '_' + sensor_name + '_' + '2', '2_std',
                                           prefix + '_' + sensor_name + '_' + '3', '3_std'])

            elif sensor_name == 'sg2_hrt':
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_1_stdev,
                                                   all_2, all_2_stdev,
                                                   all_3, all_3_stdev,
                                                   all_4, all_4_stdev]),
                                  columns=['time',
                                           prefix + '_' + sensor_name + '_' + '1', '1_std',
                                           prefix + '_' + sensor_name + '_' + '2', '2_std',
                                           prefix + '_' + sensor_name + '_' + '3', '3_std',
                                           prefix + '_' + sensor_name + '_' + '4', '4_std'])
            elif sensor_name == 'sg2_ped':
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_1_stdev,
                                                   all_2, all_2_stdev,
                                                   all_3, all_3_stdev,
                                                   all_4, all_4_stdev,
                                                   all_5, all_5_stdev,
                                                   all_6, all_6_stdev,
                                                   all_7, all_7_stdev,
                                                   all_8, all_8_stdev]),
                                  columns=['time',
                                           prefix + '_' + sensor_name + '_' + 'steps', 'steps_std',
                                           prefix + '_' + sensor_name + '_' + 'WalkingSteps', 'W_St_std',
                                           prefix + '_' + sensor_name + '_' + 'RunningSteps', 'RS_std',
                                           prefix + '_' + sensor_name + '_' + 'MovingDistance', 'MD_std',
                                           prefix + '_' + sensor_name + '_' + 'CaloriesBurned', 'CB_std',
                                           prefix + '_' + sensor_name + '_' + 'LastSpeed', 'LS_std',
                                           prefix + '_' + sensor_name + '_' + 'LastSteppingFrequency', 'LSF_std',
                                           prefix + '_' + sensor_name + '_' + 'LastPedestrianState', 'LPS_std'])
            else:
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_1_stdev]),
                                  columns=['time',
                                           sensor_name + '_' + '1', '1_stdev'])

            df.sort_values('time', inplace=True)
            df_collection[index] = df
            index += 1
            # df.to_excel('A4accAll.xlsx')
            # df.to_csv('All.csv', index=False)
            # df.to_csv('AllAcc.csv', index=False)
            file.close()
    # merge data frames:
    all_df = merge(df_collection)
    print("here")
