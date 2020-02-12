from sensorSeparator import separate
from fileCompressor import compress
from csvCreator import features_to_csv
from os import mkdir, listdir
from os.path import isfile, join
from jsonTokenizer import evening_protocols_to_csv


def separate_sensor_data(files, input_files_path, output_files_path, sensor_labels, prefix_1, prefix_2):
    try:
        # Create target Directory
        mkdir(output_files_path)
        print("Directory ", output_files_path, " Created ")
    except FileExistsError:
        print("Directory ", output_files_path, " already exists")

    separated_files = [f for f in listdir(output_files_path) if isfile(join(output_files_path, f)) & f.endswith('.txt')]
    if len(separated_files) == 0:
        separate(input_files_path, files, prefix_1, prefix_2, output_files_path, sensor_labels)
        print('separation finished')
        return True
    else:
        print('files are already separated')
        return False


def compress_fluffs(out_put_path, sensor_labels):
    # validate results
    # compress('A4-6C-F1-A0-2A-40_sg2_ped.txt', output_dir=out_put_path, file_path=out_put_path)
    # # f = 'A4-6C-F1-A0-2A-40_sg2_gps_compressed.txt'
    separated_files = [f for f in listdir(out_put_path) if isfile(join(out_put_path, f))
                       & ('compressed' not in f)
                       & f.endswith('.txt')]
    length = len(separated_files)
    if length != (len(sensor_labels) * 2 - 2):
        print('files are not separated correctly, can not compress')
        return False
    else:
        print('separation sounds nice')
        index = 1
        for f in separated_files:
            print(str(index) + ' out of ' + str(length))
            print('compressing ' + f)
            compress(f, output_dir=out_put_path, file_path=out_put_path)
            index += 1
        return True


def sensor_data_to_csv(out_put_path, prefix_1, prefix_2, sensor_labels, components=1):
    """
    convert sensor data to csv file
    :param out_put_path: where to put the .csv file
    :param prefix_1: sensor prefix one
    :param prefix_2: sensor prefix two
    :param sensor_labels:
    :param components: a flag to choose whether to convert the two sensor prefixes of just one of them,
     as the conversion is very time-costly.
    """
    # validate results
    compressed_files_x = [f for f in listdir(out_put_path)
                          if isfile(join(out_put_path, f)) & f.startswith(prefix_1) & f.endswith('compressed.txt')]
    compressed_files_y = [f for f in listdir(out_put_path)
                          if isfile(join(out_put_path, f)) & f.startswith(prefix_2) & f.endswith('compressed.txt')]
    if (len(compressed_files_x) + len(compressed_files_y)) != len(sensor_labels) * 2:
        print('\nfiles are not compressed correctly')
    else:
        print('\ncompression sounds nice')
        features_to_csv(compressed_files_x, prefix_1, file_path=out_put_path)
        if components == 2:
            features_to_csv(compressed_files_y, prefix_2, file_path=out_put_path)
        print('\nAll to_csv finished')


def combine_sd_and_ep(sensor_data_df, evening_protocols_df):
    pass


def run_pipeline():
    # patient = 'ST-1441993385'
    # prefix_1 = 'A4-6C-F1-A0-2A-40'
    # prefix_2 = 'A4-6C-F1-09-C9-31'
    patient = 'ST-1233329802'
    prefix_1 = '14-9F-3C-DA-5B-26'
    prefix_2 = 'A4-6C-F1-A0-2A-1C'
    root = '/Volumes/hex/' + patient
    fluff_txt_path = root + '-txt'
    fluff_txt_files = [f for f in listdir(fluff_txt_path) if isfile(join(fluff_txt_path, f)) & f.endswith('.txt')]
    # labels = ['sg2_acc', 'sg2_hrt', 'sg2_gyr', 'sg2_ple', 'sg2_ped', 'sg2_bar', 'sg2_gps']
    labels = ['sg2_acc', 'sg2_hrt', 'sg2_gyr', 'sg2_ple', 'sg2_ped', 'sg2_bar']

    # labels = ['sg2_gps']
    result_path = root + '-res'
    evening_protocols_path = '/Users/Hesham/dev/fluffDecoder/' + patient
    #
    # if separate(fluff_txt_files, fluff_txt_path, result_path, labels,  prefix_1, prefix_2):
    #     if compress(result_path, labels):
    #         to_csv(result_path, prefix_1, prefix_2, labels)
    # evening_protocols_to_csv(evening_protocols_path, extended_features=True)
    # separate_sensor_data(fluff_txt_files, fluff_txt_path, result_path, labels, prefix_1, prefix_2)
    # compress_fluffs(result_path, labels)
    # sensor_data_to_csv(result_path, prefix_1, prefix_2, labels)
    evening_protocols_to_csv(evening_protocols_path, result_path, patient,  extended_features=True)


# start the big bang
run_pipeline()
