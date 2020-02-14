import pandas as pd
from csvCreator import compare_string_dates
from csvCreator import extend_evening_protocols

root = '/Volumes/hex/ST-1476193030-res/'


def drop_nan(df):
    time_and_window = df.loc[:, 'time':'window']
    # rest_values = df.loc[:, 'accX':'ple_std']
    rest_labels = df.loc[:, 'alc':'phq_2']

    # 1- get indices where all elements are NaN
    idx = rest_labels.index[rest_labels.isnull().all(1)]
    # nans = rest_values.loc[idx]

    # 2- drop those elements
    file_nan_free = df.drop(idx)
    file_nan_free.to_csv(root + 'complete_2.0.csv', index=False)
    rv_nan_free = rest_labels.dropna(how='all')
    # 3- make sure both have the same number of rows
    print(file_nan_free.shape)
    print(rv_nan_free.shape)


# prefix = '14-9F-3C-DA-5B-26'
# root = '/Volumes/hex/ST-1233329802-res/'
prefix = 'A4-6C-F1-18-7D-81'


# features has to be imputed first
# features = pd.read_csv(root + prefix + '_imputed.csv')
# evening_protocols = pd.read_csv(root + 'evening_protocols.csv')
#
# # both files has to start form the same date
# extend_evening_protocols(features, evening_protocols, root)
# extended_eps = pd.read_csv(root + 'evening_protocols_extended.csv')
# completed = pd.concat([features, extended_eps], axis=1, sort=False)
# completed.to_csv(root + 'complete_1.0.csv', index=False)
complete_1 = pd.read_csv(root + 'complete_1.0.csv')
print(len(complete_1.index))
drop_nan(complete_1)

# drop missing entries
# complete_2 = pd.read_csv(root + 'complete_1.0.csv').dropna(how='all')
# print(len(complete_2.index))
# complete_2.to_csv(root + 'complete_2.0.csv', index=False)
print("done")
