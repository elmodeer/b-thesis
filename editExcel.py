import pandas as pd
import numpy as np
from csvCreator import extend_evening_protocols
from sklearn.impute import SimpleImputer

patient = 'ST1814523348'
prefix = 'A4-6C-F1-A0-28-E0'
root = '/Volumes/hex/' + patient + '-res/'


def drop_nan_in_sensor_data(df):
    # time_and_window = df.loc[:, 'time':'window']
    rest_values = df.loc[:, 'accX':'ple_std']
    # 1- get indices where all elements are NaN
    idx = rest_values.index[rest_values.isnull().all(1)]

    # 2- drop those elements
    file_nan_free = df.drop(idx)
    rv_nan_free = rest_values.dropna(how='all')
    # 3- make sure both have the same number of rows
    print(file_nan_free.shape)
    print(rv_nan_free.shape)
    return file_nan_free


def drop_nans_in_complete_df(df):
    # time_and_window = df[['time']]
    rest_labels = df.loc[:, 'alc':'phq_2']

    # 1- get indices where all elements are NaN
    idx = rest_labels.index[rest_labels.isnull().all(1)]

    # 2- drop those elements
    file_nan_free = df.drop(idx)
    rv_nan_free = rest_labels.dropna(how='all')
    # 3- make sure both have the same number of rows
    print(file_nan_free.shape)
    print(rv_nan_free.shape)
    return file_nan_free


# delete below 30 sec window
# window column has to be added manually in order for this to work. This step can be ignored if not needed specifically
def drop_below_30(df):
    print(len(df.index))
    indexNames = df[(df['window'] < 30)].index
    df.drop(indexNames, inplace=True)
    print(len(df.index))
    return df


# sd -> Sensor data, ep -> evening protocols
def drop_and_impute(features, e_protocols):
    # features = drop_below_30(features)
    # drop NaN in sensor data
    sd_nan_free = drop_nan_in_sensor_data(features)
    impute_sensor_data = SimpleImputer(strategy='median')
    impute_sensor_data.fit(sd_nan_free)
    sd_imputed = impute_sensor_data.transform(sd_nan_free)

    # extract the date column
    ep_date = e_protocols[['date']]
    # extract the rest of the values to impute them. Should be edited if different features are used.
    ep_rest_values = e_protocols.loc[:, 'alc':'phq_2']
    impute_ev_protocols = SimpleImputer(strategy='median')
    impute_ev_protocols.fit(ep_rest_values)
    ep_imputed = impute_ev_protocols.transform(ep_rest_values)
    # convert back to data frame
    ep_imputed = pd.DataFrame(ep_imputed, columns=ep_rest_values.columns,
                                        index=ep_rest_values.index)
    # recombine the imputed features with the date.
    ep_imputed = pd.concat([ep_date, ep_imputed], axis=1)

    # write the contents to two new files.
    pd.DataFrame(sd_imputed, columns=sd_nan_free.columns,
                 index=sd_nan_free.index).to_csv(root + prefix + '_imputed.csv', index=False)
    pd.DataFrame(ep_imputed, columns=e_protocols.columns,
                 index=e_protocols.index).to_csv(root + 'evening_protocols_imputed.csv', index=False)


# Read features and evening protocols
raw_sd = pd.read_csv(root + prefix + '.csv')
evening_protocols = pd.read_csv(root + 'evening_protocols.csv')

# drop NaN values and impute the sets
drop_and_impute(raw_sd, evening_protocols)
# read the imputed values
sd_imputed = pd.read_csv(root + prefix + '_imputed.csv')
evening_protocols_imputed = pd.read_csv(root + 'evening_protocols_imputed.csv')

# ==========================================================================================
# IN ORDER FOR THE NEXT FUNCTION CALL TO WORK PROPERLY, MAKE SURE THAT BOTH THE IMPUTED SENSOR DATA FILE AND THE
# EVENING PROTOCOL FILE START WITH SAME DATE.
# ==========================================================================================
extend_evening_protocols(sd_imputed, evening_protocols_imputed, root)
extended_eps = pd.read_csv(root + 'evening_protocols_extended.csv')
completed = pd.concat([sd_imputed, extended_eps], axis=1, sort=False)

# drop nan
completed = drop_nans_in_complete_df(completed)
completed.to_csv(root + patient + '_1.0.csv', index=False)
# complete_1 = pd.read_csv(root + patient + '_1.0.csv')
print("done")

