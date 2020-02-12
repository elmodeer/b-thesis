import pandas as pd
from csvCreator import compare_string_dates
from csvCreator import combine_features_and_labels
name = 'A4-6C-F1-A0-2A-40'

# file = pd.read_csv('/Users/Hesham/dev/fluffDecoder/' + name + '.csv')
# indices = file[(file['window'] < 10)].index
# file_trimmed = file.drop(indices)
# file_trimmed = file_trimmed.drop(columns=['Latitude', 'Longitude'])
# file_trimmed.to_csv(name + '_trimmed.csv', index=False)
# trim_df(file)


features = pd.read_csv('/Users/Hesham/dev/python-sandbox/last.csv')
labels = pd.read_csv('/Users/Hesham/dev/python-sandbox/labels_last.csv')
duplicated_labels = pd.read_csv('/Users/Hesham/dev/fluffDecoder/final.csv')

complete = pd.concat([features, duplicated_labels], axis=1, sort=False)

# complete.to_csv('complete_1.0.csv', index=False)
print("done")
# combine_features_and_labels(features, labels)
