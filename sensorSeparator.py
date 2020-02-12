import re

def separate(path, files, prefix_1, prefix_2, output_dir, labels):
    """
    separate .txt fluff files into individual sensor files for separate day and night.
    :param path: path to files folder
    :param files: list of files to be processed
    :param prefix_1: day files prefix
    :param prefix_2: night files prefix
    :param output_dir: patient code to create a directory with the same name
    :param labels: sensor names to separate
    """
    files.sort()
    print(len(files))

    for fluff in files:
        print(fluff)
        fileName = fluff.split('_')
        # get just the unix time part of the file name len('000.txt') = 7
        unixTime = fileName[1][:-7]
        with open(path + '/' + fluff, 'r') as myfile:
            content = myfile.read()
        x = re.split('\n', content)

        # 97 is the number of lines for a default file, if it is not so, then problems may occur.
        if len(x) != 97:
            print(fluff + ' , ', len(x))
        if fluff.startswith(prefix_1):
            time = prefix_1
        else:
            time = prefix_2
        for line in x:
            elements = re.split(':', line)
            sensor_name = elements[0].strip()
            if not sensor_name.startswith('sg2'):
                # print('could not be right')
                continue
            if sensor_name in labels:
                output_name = output_dir + '/' + time + '_' + sensor_name
                if sensor_name == 'sg2_gps':
                    sensor = open(output_name + '_compressed' + '.txt', 'a+')
                else:
                    sensor = open(output_name + '.txt', 'a+')
                    if elements[1].strip() == 'uint64':
                        sensor.write(unixTime + '\n')
                sensor.write(elements[0] + ':' + elements[2])
                sensor.write('\n')
                sensor.close()
