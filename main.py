from sensorSeparator import separate
from fileCompressor import compress
from csvCreator import to_csv
from os import getcwd, listdir
from os.path import isfile, join

patient = 'ST-1441993385'
prefix_1 = 'A4-6C-F1-A0-2A-40'
prefix_2 = 'A4-6C-F1-09-C9-31'
root = '/Volumes/hex/' + patient
my_path = root + '-txt'
all_files = [f for f in listdir(my_path) if isfile(join(my_path, f)) & f.endswith('.txt')]
#
# # separate sensor files
labels = ['sg2_acc', 'sg2_hrt', 'sg2_gyr', 'sg2_ple', 'sg2_ped', 'sg2_bar', 'sg2_gps']
# labels = ['sg2_acc']
result_path = root + '-res'
separated_files = [f for f in listdir(result_path) if isfile(join(result_path, f)) & f.endswith('.txt')]
if len(separated_files) == 0:
    separate(my_path, all_files, 'A4-6C-F1-A0-2A-40', 'A4-6C-F1-09-C9-31', '/Volumes/hex/' + patient + '-res', labels)
    print('separation finished')
else:
    print('files are already separated')

# validate results
out_put_path = '/Volumes/hex/' + patient + '-res'
# compress('A4-6C-F1-A0-2A-40_sg2_ped.txt', output_dir=out_put_path, file_path=out_put_path)
# # f = 'A4-6C-F1-A0-2A-40_sg2_gps_compressed.txt'
# result_files = [f for f in listdir(out_put_path) if isfile(join(out_put_path, f))
#                 & ('compressed' not in f)
#                 & f.endswith('.txt')]
# length = len(result_files)
# if length != (len(labels) * 2 - 2):
#     print('files are not separated correctly, can not compress')
# else:
#     print('separation sounds nice')
#     index = 0
#     for f in result_files:
#         print(str(index) + ' out of ' + str(length))
#         print(f + 'started')
#         compress(f, output_dir=out_put_path, file_path=out_put_path)
#         print(f + ' has finished')
#         index += 1

# validate results
compressed_files_x = [f for f in listdir(out_put_path)
                      if isfile(join(out_put_path, f)) & f.startswith(prefix_1) & f.endswith('compressed.txt')]
compressed_files_y = [f for f in listdir(out_put_path)
                      if isfile(join(out_put_path, f)) & f.startswith(prefix_2) & f.endswith('compressed.txt')]
if (len(compressed_files_x) + len(compressed_files_y)) != len(labels) * 2:
    print('files are not compressed correctly')
else:
    print('compression sounds nice')
    to_csv(compressed_files_x, prefix_1, file_path=out_put_path)
    # to_csv(compressed_files_y, prefix_2, file_path=out_put_path)
    # for f in compressed_files:
    #     print('starting ' + f)
    #     to_csv(f, file_path=out_put_path)
    #     print(f + ' has finished')
    print('All to_csv finished')

# generate CSV
