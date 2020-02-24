import pandas as pd
from csvCreator import get_readable_date
import numpy as np


def to_evenly_spaced(df):
    df.drop(['phq_2'], axis=1, inplace=True)
    date = df['time'].apply(lambda x: get_readable_date(x))
    df.insert(loc=1, column='date', value=date)
    median = np.trunc(df.groupby('date').size().median())
    df.drop(['date'], axis=1, inplace=True)
    day = np.trunc(len(df.index) / median)
    new_last_index = int(median * day)

    even_time = []
    firs_time = df[['time']].iloc[1].item()
    for i in range(len(df.index)):
        even_time.append(firs_time)
        firs_time += 60
    df.drop(['time'], axis=1, inplace=True)
    df.insert(loc=0, column='time', value=even_time)
    df = df.iloc[:new_last_index]
    return df, int(median)


def generator(data, look_b, delay, min_index, max_index,
              shuffle=False, batch_size=128, step=6):
    if max_index is None:
        max_index = len(data) - delay - 1
    i = min_index + look_b
    while 1:
        if shuffle:
            rows = np.random.randint(
                min_index + look_b, max_index, size=batch_size)
        else:
            if i + batch_size >= max_index:
                i = min_index + look_b
            rows = np.arange(i, min(i + batch_size, max_index))
            i += len(rows)

        samples = np.zeros((len(rows),
                           look_b // step,
                           data.shape[-1]))
        targets = np.zeros((len(rows),))
        for j, row in enumerate(rows):
            indices = range(rows[j] - look_b, rows[j], step)
            samples[j] = data[indices]
            targets[j] = data[rows[j] + delay][1]
        yield samples, targets


output_path = '/Volumes/hex/ST-1233329802-res/'
p_802 = pd.read_csv(output_path + 'ST-1233329802_3.0.csv')
# just numerical data
p_802 = p_802.drop(['date', 'window'], axis=1)
p_802, median = to_evenly_spaced(p_802)
# p_802.to_csv('p_802.csv', index=False)
# print('done')


float_data = p_802.to_numpy()

# first 200 days as training
mean = float_data[:90400].mean(axis=0)
float_data -= mean
std = float_data[:90400].std(axis=0)
float_data /= std


# assume each day got 408 value (average value) that means 17 value per Hour.
# most probably will be 3
step = int(np.trunc(60 / (median / 24)))
# observations will look back 7 days (average)
look_back = step * 7 * 24
delay = 24 * step
# one day
batch_size = median

train_gen = generator(float_data,
                      look_b=look_back,
                      delay=delay,
                      min_index=0,
                      max_index=90400,
                      shuffle=True,
                      step=step,
                      batch_size=batch_size)
val_gen = generator(float_data,
                    look_b=look_back,
                    delay=delay,
                    min_index=90401,
                    max_index=108480,
                    step=step,
                    batch_size=batch_size)
test_gen = generator(float_data,
                     look_b=look_back,
                     delay=delay,
                     min_index=108481,
                     max_index=None,
                     step=step,
                     batch_size=batch_size)

val_steps = (108480 - 90401 - look_back)
test_steps = (len(float_data) - 108481 - look_back)


def evaluate_naive_model():
    batch_maes = []
    for step in range(val_steps):
        samples, targets = next(val_gen)
        preds = samples[:, -1, 1]
        mae = np.mean(np.abs(preds - targets))
        batch_maes.append(mae)
    print(np.mean(batch_maes))


# evaluate_naive_model()
# = 1.04
