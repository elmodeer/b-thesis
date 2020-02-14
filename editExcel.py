import pandas as pd
from csvCreator import compare_string_dates
from csvCreator import extend_evening_protocols


# prefix = '14-9F-3C-DA-5B-26'
# root = '/Volumes/hex/ST-1233329802-res/'
prefix = 'A4-6C-F1-18-7D-81'
root = '/Volumes/hex/ST-1476193030-res/'


# features has to be imputed first
features = pd.read_csv(root + prefix + '_imputed.csv')
evening_protocols = pd.read_csv(root + 'evening_protocols.csv')

# both files has to start form the same date
extend_evening_protocols(features, evening_protocols, root)
extended_eps = pd.read_csv(root + 'evening_protocols_extended.csv')
completed = pd.concat([features, extended_eps], axis=1, sort=False)
completed.to_csv(root + 'complete_1.0.csv', index=False)


# drop missing entries
# completed_2 = pd.read_csv(root + 'complete_1.0.csv').dropna()
# completed_2.to_csv(root + 'complete_2.0.csv', index=False)
print("done")
