# Displays all wifi names and passwords saved to a Windows device.

import subprocess
import re
import os

wifiNamePasswordDict = {}
wifiNameRegex = re.compile(r'(?<=All User Profile     : )[\w\s\d#-\'\"@$€|%&.,~₺<!?>*+:;-]+(?=\\r\\n)')
passwordRegex = re.compile(r'(?<=Key Content            : )[\w\s\d#-\'\"@$€|%&.,~₺<!?>*+:;-]+(?=\\r\\n)')

print('\nWorking on it...')

getUser = subprocess.run(
    ['echo', '%USERNAME%'],
    stdout=subprocess.PIPE, shell=True).stdout

user = getUser.decode('UTF-8')[:-2]

getWifiNames = str(subprocess.run(
    ['netsh', 'wlan', 'show', 'profiles'],
    stdout=subprocess.PIPE, shell=True).stdout)

wifiNamesList = wifiNameRegex.findall(getWifiNames)

for wifiName in wifiNamesList:
    getPassword = str(subprocess.run(
        ['netsh', 'wlan', 'show', 'profile', wifiName, 'key=clear'],
        stdout=subprocess.PIPE, shell=True).stdout)
    try:
        password = passwordRegex.search(getPassword).group()
        wifiNamePasswordDict[wifiName] = password
    except AttributeError:
        wifiNamePasswordDict[wifiName] = 'NO PASSWORD'

os.system('cls')

print(f'\n--- Wi-Fi Names and Passwords for {user} ---\n')
for index, (wifiId, wifiPassword) in enumerate(wifiNamePasswordDict.items(), 1):
    print(f'{index}. {wifiId}: {wifiPassword}\n')

input()
