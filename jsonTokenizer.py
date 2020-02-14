import json
from os import listdir
from os.path import isfile, join
import pandas as pd


def insert_line(df, date=None, job=None, l_sit=None, age=None, alc=None, cig=None, mood=None, tense=None,
                tired=None, period=None, rumination=None, socialize=None, socialize_val=None,
                sport_time=None, work_time=None, day_sleep=None, phq_1=None, phq_2=None):
    df = df.append({'date': date,'job': job, 'l_sit': l_sit,
                    'age': age, 'alc': alc, 'cig': cig,
                    'mood': mood, 'tense': tense, 'tired': tired, 'period': period,
                    'rumination': rumination, 'socialize': socialize, 'socialize_val': socialize_val,
                    'sport_time': sport_time, 'work_time': work_time,
                    'day_sleep': day_sleep, 'phq_1': phq_1, 'phq_2': phq_2}, ignore_index=True)

    return df


def get_date(param):
    parts = param.split('-')
    return parts[2] + '.' + parts[1] + '.' + parts[0][2:]


def evening_protocols_to_csv(input_path, result_path, extended_features=False):
    files = [f for f in listdir(input_path) if isfile(join(input_path, f))
             & ('EVENING' in f)
             & f.endswith('.json')]
    files.sort()
    complete_df = pd.DataFrame(columns=['date', 'job', 'l_sit', 'age', 'alc', 'cig', 'mood', 'tense',
                                        'tired', 'period', 'rumination', 'socialize', 'socialize_val',
                                        'sport_time', 'work_time', 'day_sleep', 'phq_1', 'phq_2'])
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
            profile = data['profile']
            phq_1 = data['PHQ2_1']
            phq_2 = data['PHQ2_2']
            if extended_features:
                date = get_date(json_content['date'])
                gender = profile['gender']
                job = profile['job']
                living_situation = profile['livingSituation']
                age = 2020 - int(profile['yearOfBirth'])
                # medication  ??? and alcohol and cigarettes and day sleep
                alc = data['alc']
                cig = data['cig']
                mood = data['mood']
                tense = data['tense']
                tired = data['tired']
                if gender == 'FEMALE':
                    if data['period'] == 'true':
                        period = 1
                    else:
                        period = 0
                else:
                    period = 'NULL'
                rumination = data['rumination']
                socialize = data['socialize']
                socialize_val = data['socialize_val']
                sport_time = data['sport']['time']
                work_time = data['work']['time']
                day_sleep = data['daySleep']['DS_TST']

                complete_df = insert_line(complete_df, date, job, living_situation, age, alc, cig, mood, tense,
                                          tired, period, rumination, socialize, socialize_val, sport_time, work_time,
                                          day_sleep, phq_1, phq_2)
            else:
                complete_df = insert_line(complete_df, phq_1, phq_2)

            evening_protocol.close()
    complete_df.to_csv(result_path + '/evening_protocols_O.csv', index=False)
    complete_df.to_csv(result_path + '/evening_protocols.csv', index=False)
