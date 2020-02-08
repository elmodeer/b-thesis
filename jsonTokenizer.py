import json
from os import listdir
from os.path import isfile, join
import pandas as pd


def insert_line(df, date=None, gender=None, l_sit=None, age=None, alc=None, cig=None, mood=None, tense=None,
                tired=None, period=None, rumination=None, socialize=None, phq_1=None, phq_2=None):
    df = df.append({'date': date, 'gender': gender, 'l_sit': l_sit,
                    'age': age, 'alc': alc, 'cig': cig,
                    'mood': mood, 'tense': tense, 'tired': tired, 'period': period,
                    'rumination': rumination, 'socialize': socialize,
                    'phq_1': phq_1, 'phq_2': phq_2}, ignore_index=True)

    return df


def get_labels(files, input_path, extended_features=False):
    files.sort()

    complete_df = pd.DataFrame(columns=['date', 'gender', 'l_sit', 'gender', 'age', 'alc', 'cig', 'mood', 'tense',
                                        'tired', 'period', 'rumination', 'socialize', 'phq_1', 'phq_2'])
    for file in files:
        print(file)
        with open(input_path + '/' + file, 'rt') as evening_protocol:
            content = evening_protocol.read()
            content = content.replace("\'", "\"")
            content = content.replace("\"contents\": \"{", "\"contents\": {")
            content = content.replace("}\"", "}")
            json_content = json.loads(content)
            # extracting features
            data = json_content['contents']
            phq_1 = data['PHQ2_1']
            phq_2 = data['PHQ2_2']
            if extended_features:
                date = data['date']
                gender = data['gender']
                living_situation = data['livingSituation']
                age = 2020 - int(data['yearOfBirth'])
                # medication  ???
                alc = data['alc']
                cig = data['cig']
                mood = data['mood']
                tense = data['tense']
                tired = data['tired']
                if gender == 'FEMALE':
                    period = data['period']
                else:
                    period = 'NULL'
                rumination = data['rumination']
                socialize = data['socialize']
                insert_line(complete_df, date, gender, living_situation, age, alc, cig, mood, tense,
                            tired, period, rumination, socialize, phq_1, phq_2)
            else:
                insert_line(complete_df, phq_1, phq_2)

            evening_protocol.close()
    return complete_df


patient = 'ST-1441993385'
my_path = '/Users/Hesham/dev/fluffDecoder/' + patient
all_files = [f for f in listdir(my_path) if isfile(join(my_path, f)) & f.endswith('.json')]
co_df = get_labels(all_files, my_path)
print('sadfasdf')