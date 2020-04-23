import subprocess
import pandas as pd
import numpy as np
from datetime import datetime
import math
import operator

from re import split
import re
from fluffUtil import get_sensor_name, get_lines_to_read, get_values, match_unix_stamp


# shall be adapted if sensor data is changed
def insert_line(df, dict):
    df = df.append({'time': dict.get('time'),
                    'accX': dict.get('accX'), 'accX_std': dict.get('accX_std'),
                    'accY': dict.get('accY'), 'accY_std': dict.get('accY_std'),
                    'accZ': dict.get('accZ'), 'accZ_std': dict.get('accZ_std'),

                    'gyrX': dict.get('gyrX'), 'gyrX_std': dict.get('gyrX_std'),
                    'gyrY': dict.get('gyrY'), 'gyrY_std': dict.get('gyrY_std'),
                    'gyrZ': dict.get('gyrZ'), 'gyrZ_std': dict.get('gyrZ_std'),

                    'heartR': dict.get('heartR'), 'heartR_std': dict.get('heartR_std'),

                    'SmoothedAirPressure': dict.get('SmoothedAirPressure'), 'SAP_std': dict.get('SAP_std'),
                    'UncalibratedBarometerAltitude': dict.get('UncalibratedBarometerAltitude'),
                    'UBA_std': dict.get('UBA_std'),
                    'AirTemperature': dict.get('AirTemperature'), 'AT_std': dict.get('AT_std'),
                    'AirPressure': dict.get('AirPressure'), 'AP_std': dict.get('AP_std'),

                    'PlethysmogramGreen': dict.get('PlethysmogramGreen'), 'ple_std': dict.get('ple_std'),

                    'steps': dict.get('steps'), 'steps_std': dict.get('steps_std'),
                    'WalkingSteps': dict.get('WalkingSteps'), 'W_St_std': dict.get('W_St_std'),
                    'RunningSteps': dict.get('RunningSteps'), 'RS_std': dict.get('RS_std'),
                    'CaloriesBurned': dict.get('CaloriesBurned'), 'CB_std': dict.get('CB_std'),

                    'Latitude': dict.get('Latitude'),
                    'Longitude': dict.get('Longitude'),
                    }, ignore_index=True)

    return df


#  get next earliest date
def get_next_earliest(df_collection):
    # get earliest data frame
    temp_dict = {}
    for key in df_collection:
        if len(df_collection[key]) != 0:
            temp_dict[key] = df_collection[key]['time'].iloc[0]
    if len(temp_dict) != 0:
        earliest_key = min(temp_dict, key=temp_dict.get)
    else:
        return 0, 'none'
    earliest_time = df_collection[earliest_key]['time'].iloc[0]
    return earliest_time, earliest_key


def get_latest(df_collection):
    temp_dict = {}
    for key in df_collection:
        if len(df_collection[key]) != 0:
            temp_dict[key] = df_collection[key]['time'].iloc[-1]
    if len(temp_dict) != 0:
        latest_key = max(temp_dict, key=temp_dict.get)
    else:
        return 0, 'none'
    latest_time = df_collection[latest_key]['time'].iloc[0]
    return latest_time, latest_key


def df_collection_is_not_empty(df_collection):
    for key in df_collection:
        if len(df_collection[key]) != 0:
            return True
        else:
            continue
    return False


def merge(df_collection):
    complete_df = pd.DataFrame(columns=['time',
                                        # acc
                                        'accX', 'accX_std',
                                        'accY', 'accY_std',
                                        'accZ', 'accZ_std',

                                        'gyrX', 'gyrX_std',
                                        'gyrY', 'gyrY_std',
                                        'gyrZ', 'gyrZ_std',

                                        'heartR', 'heartR_std',

                                        'SmoothedAirPressure', 'SAP_std',
                                        'UncalibratedBarometerAltitude', 'UBA_std',
                                        'AirTemperature', 'AT_std',
                                        'AirPressure', 'AP_std',

                                        'PlethysmogramGreen', 'ple_std',

                                        'steps', 'steps_std',
                                        'WalkingSteps', 'W_St_std',
                                        'RunningSteps', 'RS_std',
                                        'CaloriesBurned', 'CB_std',

                                        'Latitude',
                                        'Longitude'])

    # start two minutes aggregating
    earliest_time, key = get_next_earliest(df_collection)
    # latest_time, l_key = get_latest(df_collection)
    while df_collection_is_not_empty(df_collection):
        merging_keys = []
        limit = earliest_time + 61
        for key in df_collection:
            if len(df_collection[key]) != 0:
                if df_collection[key]['time'].iloc[0] <= limit:
                    merging_keys.append(key)
        # combine new row
        temp_dict = {'time': earliest_time}
        for key in merging_keys:
            if key == 'sg2_bar':
                if len(df_collection[key].index) != 0:
                    temp_dict['SmoothedAirPressure'] = df_collection[key]['SmoothedAirPressure'].iloc[0]
                    temp_dict['UncalibratedBarometerAltitude'] = df_collection[key]['UncalibratedBarometerAltitude'].iloc[0]
                    temp_dict['AirTemperature'] = df_collection[key]['AirTemperature'].iloc[0]
                    temp_dict['AirPressure'] = df_collection[key]['AirPressure'].iloc[0]
                    temp_dict['SAP_std'] = df_collection[key]['SAP_std'].iloc[0]
                    temp_dict['UBA_std'] = df_collection[key]['UBA_std'].iloc[0]
                    temp_dict['AT_std'] = df_collection[key]['AT_std'].iloc[0]
                    temp_dict['AP_std'] = df_collection[key]['AP_std'].iloc[0]
                    # drop this row
                    df_collection[key] = df_collection[key].iloc[1:]
                else:
                    del df_collection[key]
            if key == 'sg2_gps':
                if len(df_collection[key].index) != 0:
                    temp_dict['Latitude'] = df_collection[key]['Latitude'].iloc[0]
                    temp_dict['Longitude'] = df_collection[key]['Longitude'].iloc[0]
                    # drop this row
                    df_collection[key] = df_collection[key].iloc[1:]
                else:
                    del df_collection[key]
            if key == 'sg2_acc':
                if len(df_collection[key].index) != 0:
                    temp_dict['accX'] = df_collection[key]['X'].iloc[0]
                    temp_dict['accY'] = df_collection[key]['Y'].iloc[0]
                    temp_dict['accZ'] = df_collection[key]['Z'].iloc[0]
                    temp_dict['accX_std'] = df_collection[key]['x_std'].iloc[0]
                    temp_dict['accY_std'] = df_collection[key]['y_std'].iloc[0]
                    temp_dict['accZ_std'] = df_collection[key]['y_std'].iloc[0]
                    # drop this row
                    df_collection[key] = df_collection[key].iloc[1:]
                else:
                    del df_collection[key]
            if key == 'sg2_ple':
                if len(df_collection[key].index) != 0:
                    temp_dict['PlethysmogramGreen'] = df_collection[key]['PlethysmogramGreen'].iloc[0]
                    temp_dict['ple_std'] = df_collection[key]['ple_std'].iloc[0]
                    # drop this row
                    df_collection[key] = df_collection[key].iloc[1:]
                else:
                    del df_collection[key]
            if key == 'sg2_ped':
                if len(df_collection[key].index) != 0:
                    temp_dict['steps'] = df_collection[key]['steps'].iloc[0]
                    temp_dict['WalkingSteps'] = df_collection[key]['WalkingSteps'].iloc[0]
                    temp_dict['RunningSteps'] = df_collection[key]['RunningSteps'].iloc[0]
                    temp_dict['CaloriesBurned'] = df_collection[key]['CaloriesBurned'].iloc[0]
                    temp_dict['steps_std'] = df_collection[key]['steps_std'].iloc[0]
                    temp_dict['W_St_std'] = df_collection[key]['W_St_std'].iloc[0]
                    temp_dict['RS_std'] = df_collection[key]['RS_std'].iloc[0]
                    temp_dict['CB_std'] = df_collection[key]['CB_std'].iloc[0]
                    df_collection[key] = df_collection[key].iloc[1:]
                else:
                    del df_collection[key]
            if key == 'sg2_hrt':
                if len(df_collection[key].index) != 0:
                    temp_dict['heartR'] = df_collection[key]['heartR'].iloc[0]
                    temp_dict['heartR_std'] = df_collection[key]['heartR_std'].iloc[0]
                    df_collection[key] = df_collection[key].iloc[1:]
                else:
                    del df_collection[key]
            if key == 'sg2_gyr':
                if len(df_collection[key].index) != 0:
                    temp_dict['gyrX'] = df_collection[key]['X'].iloc[0]
                    temp_dict['gyrY'] = df_collection[key]['Y'].iloc[0]
                    temp_dict['gyrZ'] = df_collection[key]['Z'].iloc[0]
                    temp_dict['gyrX_std'] = df_collection[key]['x_std'].iloc[0]
                    temp_dict['gyrY_std'] = df_collection[key]['y_std'].iloc[0]
                    temp_dict['gyrZ_std'] = df_collection[key]['z_std'].iloc[0]
                    df_collection[key] = df_collection[key].iloc[1:]
                else:
                    del df_collection[key]
        # earliest_time = df_collection[earliest_key]['time'].iloc[0]
        earliest_time, key = get_next_earliest(df_collection)
        if not complete_df.empty:
            if earliest_time == complete_df['time'].iloc[-1]:
                print('Duplicated entry. ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR')
                continue
        print(str(earliest_time) + ' from ' + key)
        complete_df = insert_line(complete_df, temp_dict)
    return complete_df


def sensor_data_to_csv(files, prefix, file_path=''):
    df_collection = {}
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

            all_1 = []
            all_1_std = []

            all_2 = []
            all_2_std = []

            all_3 = []
            all_3_std = []

            all_4 = []
            all_4_std = []

            print(file_name)
            while window < fileLines:
                file_lines = []
                for i in range(lines_per_iteration):
                    file_lines.append(get_values(file.readline()))

                timeAll.extend(file_lines[0])
                all_1.extend(file_lines[1])
                all_1_std.extend((file_lines[2]))
                # special case
                if sensor_name == 'sg2_gps':
                    all_2.extend(file_lines[2])
                    all_3.extend(file_lines[3])
                    window += lines_per_iteration
                    continue

                if sensor_name in ['sg2_gyr', 'sg2_bar', 'sg2_acc', 'sg2_ped']:
                    all_2.extend(file_lines[3])
                    all_2_std.extend(file_lines[4])
                    all_3.extend(file_lines[5])
                    all_3_std.extend(file_lines[6])
                if sensor_name in ['sg2_bar', 'sg2_ped', 'sg2_bar']:
                    all_4.extend(file_lines[7])
                    all_4_std.extend(file_lines[8])

                # print(window)
                window += lines_per_iteration

            if sensor_name == 'sg2_acc' or sensor_name == 'sg2_gyr':
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_1_std,
                                                   all_2, all_2_std,
                                                   all_3, all_3_std]),
                                  columns=['time',
                                           'X', 'x_std',
                                           'Y', 'y_std',
                                           'Z', 'z_std'])

            elif sensor_name == 'sg2_hrt':
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_1_std]),
                                  columns=['time',
                                           'heartR', 'heartR_std'])
                indexNames = df[(df['heartR'] < 30)].index
                df.drop(indexNames, inplace=True)

            elif sensor_name == 'sg2_bar':
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_1_std,
                                                   all_2, all_2_std,
                                                   all_3, all_3_std,
                                                   all_4, all_4_std]),
                                  columns=['time',
                                           'SmoothedAirPressure', 'SAP_std',
                                           'UncalibratedBarometerAltitude', 'UBA_std',
                                           'AirTemperature', 'AT_std',
                                           'AirPressure', 'AP_std'])
            elif sensor_name == 'sg2_ped':
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_1_std,
                                                   all_2, all_2_std,
                                                   all_3, all_3_std,
                                                   all_4, all_4_std]),
                                  columns=['time',
                                           'steps', 'steps_std',
                                           'WalkingSteps', 'W_St_std',
                                           'RunningSteps', 'RS_std',
                                           'CaloriesBurned', 'CB_std'])
            elif sensor_name == 'sg2_gps':
                df = pd.DataFrame(np.column_stack([timeAll, all_1, all_2]),
                                  columns=['time',
                                           'Latitude', 'Longitude'])
                df = df[df['Latitude'] != 0]
            # when sg2_ple
            else:
                df = pd.DataFrame(np.column_stack([timeAll,
                                                   all_1, all_1_std]),
                                  columns=['time',
                                           'PlethysmogramGreen', 'ple_std'])

            df = df.sort_values('time')
            df_collection[sensor_name] = df
            file.close()
    # merge "sensor data" date frames:
    all_df = merge(df_collection)
    all_df.to_csv(file_path + '/' + prefix + '_Original.csv', index=False)
    all_df.to_csv(file_path + '/' + prefix + '.csv', index=False)


def compare_string_dates(date1, date2):
    """
    compare two dates of type String of format dd.mm.yy
    :param date1: first date
    :param date2: second date
    :return: 1 if date1 > date2 and 0 if equal and -1 if otherwise
    """
    components1 = list(map(int, date1.split('.')))
    components2 = list(map(int, date2.split('.')))

    if components1[2] == components2[2]:
        if components1[1] == components2[1]:
            if components1[0] > components2[0]:
                return 1
            elif components1[0] == components2[0]:
                return 0
            else:
                return -1
        elif components1[1] > components2[1]:
            return 1
        else:
            return -1
    elif components1[2] > components2[2]:
        return 1
    else:
        return -1


def get_readable_date(date):
    # Y for XXXX and y for XX
    # %H:%M:%S for more precision
    return datetime.utcfromtimestamp(date).strftime('%d.%m.%y')


# fill missing ranges with NaN values to be removed later
def fill_missing_range(result, features, missing_date, index):
    while index < len(features.index) and get_readable_date(features['time'].iloc[index]) == missing_date:
        result = result.append(pd.Series(), ignore_index=True)
        index += 1
    return index, result


def evening_protocols_contain_this_date(evening_protocols, date):
    for i, row in evening_protocols.iterrows():
        if row['date'] == date:
            return True
    return False


def extend_evening_protocols(sensor_data, evening_protocols, output_path):
    """
    This method is very crucial, as it extends the evening protocols set depending on the corresponding sensor data
    file. Basically, it copies the entry of a given day for the number of times this day was mentioned in the sensor
    data file.
    :param sensor_data: sensor data file
    :param evening_protocols: evening protocols fils
    :param output_path: where the result file shall be located
    :return: Extended version of the evening protocols
    """

    # the features that shall be extended. Should be edited if the features changes.
    result = pd.DataFrame(columns=['date', 'alc', 'cig', 'mood', 'tense',
                                   'tired', 'period', 'rumination', 'socialize', 'socialize_val',
                                   'sport_time', 'work_time', 'day_sleep', 'phq_1', 'phq_2'])
    j = 0
    i = 0
    f_length = len(sensor_data.index)
    l_length = len(evening_protocols.index)
    # 1- loop around the features data frame and accordingly copy the values of the evening protocols
    # 2- missing dates in the ev_protocols are filled with null values to be discarded in a later step. this work around
    # to help simplify the process of concatenating the two data frames.
    if get_readable_date(sensor_data['time'].iloc[0]) != evening_protocols['date'].iloc[0]:
        print('files does not start at the same time')
        return
    while i < f_length:
        date = get_readable_date(sensor_data['time'].iloc[i])
        evening_protocol_row = evening_protocols.iloc[j]
        if date == evening_protocol_row['date']:
            # result = result.append({'date': evening_protocol_row['date'], 'alc': evening_protocol_row['alc'],
            #                         'cig': evening_protocol_row['cig'],
            #                         'mood': evening_protocol_row['mood'], 'tense': evening_protocol_row['tense'],
            #                         'tired': evening_protocol_row['tired'], 'period': evening_protocol_row['period'],
            #                         'rumination': evening_protocol_row['rumination'],
            #                         'socialize': evening_protocol_row['socialize'],
            #                         'socialize_val': evening_protocol_row['socialize_val'],
            #                         'sport_time': evening_protocol_row['sport_time'],
            #                         'work_time': evening_protocol_row['work_time'],
            #                         'day_sleep': evening_protocol_row['day_sleep'],
            #                         'phq_1': evening_protocol_row['phq_1'], 'phq_2': evening_protocol_row['phq_2']},
            #                        ignore_index=True)

            result = result.append({'date': evening_protocol_row['date'],
                                    'mood': evening_protocol_row['mood'], 'tense': evening_protocol_row['tense'],
                                    'tired': evening_protocol_row['tired'],
                                    'rumination': evening_protocol_row['rumination'],
                                    'socialize': evening_protocol_row['socialize'],
                                    'socialize_val': evening_protocol_row['socialize_val'],
                                    'work_time': evening_protocol_row['work_time'],
                                    'day_sleep': evening_protocol_row['day_sleep'],
                                    'phq_1': evening_protocol_row['phq_1'], 'phq_2': evening_protocol_row['phq_2']},
                                   ignore_index=True)
            i += 1
        elif not evening_protocols_contain_this_date(evening_protocols, date):
            i, result = fill_missing_range(result, sensor_data, date, i)
        else:
            print('at index ' + str(j) + ' of ' + str(l_length) + ' and index ' + str(i) + ' of ' + str(f_length))
            if (j + 1) < l_length:
                j += 1
    print(j)
    print(len(sensor_data.index))
    result.to_csv(output_path + 'evening_protocols_extended.csv', index=False)
