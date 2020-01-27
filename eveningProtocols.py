from os import listdir
from os.path import isfile, join
import pandas as pd


mypath = '/Users/Hesham/dev/phq/ST-1946093440'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) & f.endswith('json')]
onlyfiles.sort()

files = []
for p in onlyfiles:
    p = p[len('ST-1946093440_EVENING_'):len('ST-1946093440_EVENING_2017-11-15')]
    files.append(p)
df = pd.DataFrame(files)
df.to_excel('evenings.xlsx')
