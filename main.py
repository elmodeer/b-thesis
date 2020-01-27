from sensorSeparator import separate
from fileCompressor import compress
from csvCreator import to_csv
from os import getcwd, listdir
from os.path import isfile, join

patient = 'ST-1441993385'
prefix_1 = 'A4-6C-F1-A0-2A-40'
prefix_2 = 'A4-6C-F1-09-C9-31'
my_path = '/Volumes/hex/' + patient + '-txt'
all_files = [f for f in listdir(my_path) if isfile(join(my_path, f)) & f.endswith('.txt')]
#
# # separate sensor files
labels = ['sg2_acc', 'sg2_hrt', 'sg2_gyr', 'sg2_ple', 'sg2_ped', 'sg2_bar', 'sg2_gps']
# gps_label = ['sg2_gps']

separate(my_path, all_files, 'A4-6C-F1-A0-2A-40', 'A4-6C-F1-09-C9-31', patient + '-res', labels)
print('separation finished')

# validate results
out_put_path = '/Users/Hesham/dev/fluffDecoder/' + patient + '-res'
# compress('A4-6C-F1-09-C9-31_sg2_bar.txt', output_dir=out_put_path, file_path=out_put_path)
#
# result_files = [f for f in listdir(out_put_path) if isfile(join(out_put_path, f)) & f.endswith('.txt')]
# if len(result_files) != (len(labels) * 2 - 1):
#     print('files are not separated correctly, can not compress')
# else:
#     print('separation sounds nice')
#     for f in result_files:
#         print('starting ' + f)
#         compress(f, output_dir=out_put_path, file_path=out_put_path)
#         print(f + ' has finished')

# validate results
# compressed_files_x = [f for f in listdir(out_put_path)
#                       if isfile(join(out_put_path, f)) & f.startswith(prefix_1) & f.endswith('compressed.txt')]
# compressed_files_y = [f for f in listdir(out_put_path)
#                       if isfile(join(out_put_path, f)) & f.startswith(prefix_2) & f.endswith('compressed.txt')]
# if (len(compressed_files_x) + len(compressed_files_y)) != len(labels) * 2:
#     print('files are not compressed correctly')
# else:
#     print('compression sounds nice')
#     to_csv(compressed_files_x, 'X', file_path=out_put_path)
#     to_csv(compressed_files_y, 'Y', file_path=out_put_path)
#     # for f in compressed_files:
#     #     print('starting ' + f)
#     #     to_csv(f, file_path=out_put_path)
#     #     print(f + ' has finished')
#     print('All to_csv finished')

# generate CSV
