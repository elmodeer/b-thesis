import pandas as pd
import numpy as np
from csvCreator import extend_evening_protocols
from sklearn.impute import SimpleImputer

patient = 'ST1814523348'
prefix = 'A4-6C-F1-A0-28-E0'
root = '/Volumes/hex/' + patient + '-res/'


def drop_nan_in_raw_features(df):
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


def drop_evening_protocols_extended_nan_in_complete_df(df):
    # time_and_window = df[['time']]
    rest_labels = df.loc[:, 'alc':'phq_2']

    # 1- get indices where all elements are NaN
    idx = rest_labels.index[rest_labels.isnull().all(1)]

    # 2- drop those elements
    file_nan_free = df.drop(idx)
    # file_nan_free.to_csv(root + 'complete_2.0.csv', index=False)
    rv_nan_free = rest_labels.dropna(how='all')
    # 3- make sure both have the same number of rows
    print(file_nan_free.shape)
    print(rv_nan_free.shape)
    return file_nan_free


# # delete below 30 sec window
def drop_below_30(df):
    print(len(df.index))
    indexNames = df[(df['window'] < 30)].index
    df.drop(indexNames, inplace=True)
    print(len(df.index))
    return df


def drop_and_impute(features, ev_protocols):
    features = drop_below_30(features)
    file_nan_free = drop_nan_in_raw_features(features)
    impute_features = SimpleImputer(strategy='median')
    impute_features.fit(file_nan_free)
    file_imputed = impute_features.transform(file_nan_free)

    ev_protocols_data = ev_protocols[['date']]
    ev_protocols_rest_values = ev_protocols.loc[:, 'alc':'phq_2']
    impute_ev_protocols = SimpleImputer(strategy='median')
    impute_ev_protocols.fit(ev_protocols_rest_values)
    ev_protocols_imputed = impute_ev_protocols.transform(ev_protocols_rest_values)
    # convert back to data frame
    ev_protocols_imputed = pd.DataFrame(ev_protocols_imputed, columns=ev_protocols_rest_values.columns,
                                        index=ev_protocols_rest_values.index)
    # recombine them
    ev_protocols_imputed = pd.concat([ev_protocols_data, ev_protocols_imputed], axis=1)

    pd.DataFrame(file_imputed, columns=file_nan_free.columns,
                 index=file_nan_free.index).to_csv(root + prefix + '_imputed.csv', index=False)
    pd.DataFrame(ev_protocols_imputed, columns=ev_protocols.columns,
                 index=ev_protocols.index).to_csv(root + 'evening_protocols_imputed.csv', index=False)


# # features has to be imputed first
raw_features = pd.read_csv(root + prefix + '.csv')
evening_protocols = pd.read_csv(root + 'evening_protocols.csv')

drop_and_impute(raw_features, evening_protocols)
features_imputed = pd.read_csv(root + prefix + '_imputed.csv')
evening_protocols_imputed = pd.read_csv(root + 'evening_protocols_imputed.csv')

# both files has to start form the same date
extend_evening_protocols(features_imputed, evening_protocols_imputed, root)
extended_eps = pd.read_csv(root + 'evening_protocols_extended.csv')
completed = pd.concat([features_imputed, extended_eps], axis=1, sort=False)

# drop nan
completed = drop_evening_protocols_extended_nan_in_complete_df(completed)
completed.to_csv(root + patient + '_1.0.csv', index=False)
complete_1 = pd.read_csv(root + patient + '_1.0.csv')

print("done")

