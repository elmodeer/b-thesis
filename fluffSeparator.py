import re
from os import getcwd, listdir
from os.path import isfile, join
mypath = '/Users/Hesham/dev/data'


onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) & f.endswith('.txt')]
onlyfiles.sort()

print(len(onlyfiles))
for fluff in onlyfiles:
    print(fluff)
    fileName = fluff.split("_")
    # get just the unix time part of the file name len("000.txt") = 7
    unixTime = fileName[1][:-7]
    with open(mypath + "/" + fluff, 'r') as myfile:
        str = myfile.read()
    x = re.split("\n", str)
    if len(x) != 97:
        print(fluff + " , ", len(x))
    for line in x:
        elements = re.split(":", line)
        time = ""
        if fluff.startswith("A4"):
            time = "A4"
        else:
            time = "BC"
        if elements[0] == "sg2_acc ":
            sensor = open(time + "acc.txt", 'a+')
            if elements[1] == " uint64 ":
                sensor.write(unixTime + '\n');
            sensor.write(elements[0] + ":" + elements[2])
            sensor.write('\n')
            sensor.close()
        # # elif elements[0] == "sg2_grv":
        #     sensor = open(time + "grv.txt", 'a')
        #     sensor.write(elements[0]) + ":" + elements[2];
        #     sensor.close()
        # elif elements[0] == "sg2_grv":
        #     sensor = open(time + "grv.txt", 'a')
        #     sensor.write(elements[0]) + ":" + elements[2];
        #     sensor.close()
        # elif elements[0] == "sg2_grv":
        #     sensor = open(time + "grv.txt", 'a')
        #     sensor.write(elements[0]) + ":" + elements[2];
        #     sensor.close()
