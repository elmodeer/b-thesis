# importing the requests library 
import requests
import os
import json
import time

userID = "DemoUser"     # bei Bedarf hier Nutzernamen ändern
password = "Demo123"    # bei Bedarf hier Passwort ändern
excludedUsers = ["",""]    # hier Pseudonyme einfügen, die beim Durchlauf ausgeschlossen werden sollen

#Prod-System
ENDPOINT_DATA = "https://sci-rest.steady-projekt.de/output"
ENDPOINT_LOGIN = "https://sci-rest.steady-projekt.de/user/login"

#Lokal-System
#ENDPOINT_LOGIN = "http://localhost:8082/user/login"
#ENDPOINT_DATA = "http://localhost:8082/output"

def dl_morning(pat, base_dir, cwd):
    response = requests.get(url=ENDPOINT_DATA+"/getAllMorningProtocolsOfPatient?pseudo=" + pat, headers=header)
    print(len(response.json()))
    for protocol in response.json():
        file = open(protocol["pseudonym"]+"_MORNING_"+protocol["date"]+".json", 'w+')
        file.write(str(protocol))
    response = ""

def dl_evening(pat, base_dir, cwd):
    response = requests.get(url=ENDPOINT_DATA+"/getAllEveningProtocolsOfPatient?pseudo=" + pat, headers=header)
    print(len(response.json()))
    for protocol in response.json():
        file = open(protocol["pseudonym"]+"_EVENING_"+protocol["date"]+".json", 'w+')
        file.write(str(protocol))
    response = ""

def dl_phq(pat, base_dir, cwd):
    response = requests.get(url=ENDPOINT_DATA+"/getAllPhqProtocolsOfPatient?pseudo=" + pat, headers=header)
    print(len(response.json()))
    for protocol in response.json():
        file = open(protocol["pseudonym"]+"_PHQ_"+protocol["date"]+".json", 'w+')
        file.write(str(protocol))
    response = ""

def dl_sensors(pat, base_dir, cwd):
    response = requests.get(url=ENDPOINT_DATA+"/getAllSensorIDsOfPatient?pseudo=" + pat, headers=header)
    print(len(response.json()))
    for ID in response.json():
        singleResponse = requests.get(url=ENDPOINT_DATA+"/getSingleDocument?id=" + ID, headers=header)
        sensorFileName = singleResponse.json()["name"]
        try:
            print("" + sensorFileName)
        except TypeError:
            sensorFileName = "noNameAvailable"
        file = open(pat+"_SENSOR_"+ sensorFileName +".json", 'w+')
        file.write(str(singleResponse.json()))
    response = ""

def includesItem(list, checkItem):
    for item in list:
        if str(item) == str(checkItem):
            return True
    return False

patients = []

# JWT Auth-Token
JWT_TOKEN = "Bearer eyJjdHkiOiJKV1QiLCJlbmMiOiJBMTI4R0NNIiwiYWxnIjoiZGlyIn0..GHdSBpkWsjCf1d81.yVU8JfyL7b77JtwfVvhkiHcMz3_cCmOSIWynfEY6gN1RsUHvLu2AxDdqGg0JYjklF3XHdrLI51YVAx_wDgc_tf4y50NWp7cX8QzY0NPD26tr3FwJKl70MfAatdi08GGd1_fZA5-DAxeWWgWS9aU-SS5-LGYsVgqrpoz8XmCItM208b4aqzeOEiF3ydrAAAR_bKAoXbLPXYvX6F7r0R1KDrdx08QX-beJSyCxbevEXpQ-1xVd7ucuWwGTfUfXZWGPcJR_lmCP_hQync0wDmaIrTwjTpzo.N-638vcie10aUFJiBswnFQ"
header = {"Content-Type": "application/json"}

print("start")

print("Login with " + userID + " and " + password + " ...")
payload = json.dumps({"userID": userID, "password": password})
response = requests.post(url=ENDPOINT_LOGIN, data=payload, headers=header)
print(response.json())
JWT_TOKEN = "Bearer " + response.json()["jwt"]
header = {'Authorization': JWT_TOKEN}
print("Login successful\n")

try:
    os.mkdir("Patientendaten")
except FileExistsError:
    pass
os.chdir("Patientendaten")
cwd = os.getcwd()

print("Finding patients...")
response = requests.get(url=ENDPOINT_DATA+"/getAllPatientPseudos", headers=header)
for pseudonym in response.json():
    print("\t: " + pseudonym)
    patients.append(pseudonym)
print("Got all patients\n")

# for patient in patients:
#     if includesItem(excludedUsers, patient):
#         print("Patient skipped: " + patient)
#         continue
#     try:
#         os.mkdir(patient)
#     except FileExistsError:
#         pass
#     os.chdir(patient)


for patient in patients:
    if patient.startswith('ST1814523348'):
        chosenOne = patient
        break

patient = chosenOne
# print("Starting download of MorningProtocols for " + patient)
# dl_morning(patient, cwd, os.getcwd())
# print("Morning downloads for " + patient + " finished")
# print()

print("Starting download of EveningProtocols for " + patient)
dl_evening(patient, cwd, os.getcwd())
print("Evening downloads for " + patient + " finished")
print()

# print("Starting download of PHQProtocols for " + patient)
# dl_phq(patient, cwd, os.getcwd())
# print("PHQ downloads for " + patient + " finished")
# print()

    # print("Starting download of SensorData for " + patient)
    # dl_sensors(patient, cwd, os.getcwd())
    # print("Sensor downloads for " + patient + " finished")
    # print()

    # os.chdir(cwd)

print("end")

