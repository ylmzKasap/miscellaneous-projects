import subprocess
import re
import os

wifiNamePasswordDict = {}
passwordRegex = re.compile(r'(?<=Key Content            : )[\w\s\d#-\'\"@$€|%&.,~₺<!?>*+:;-]+(?=\\r\\n)')

print('\nWorking on it...')

getUser = subprocess.run(
    ['echo', '%USERNAME%'],
    stdout=subprocess.PIPE, shell=True).stdout

user = getUser.decode('UTF-8')[:-2]

getWifiNames = str(subprocess.run(
    ['netsh', 'wlan', 'show', 'profiles'],
    stdout=subprocess.PIPE, shell=True).stdout)

wifiNamesList = (getWifiNames.replace('\\r', '')
    .replace('\\n', '')
    .replace('\\x99', 'Ö')
    .replace('\\x94', 'ö')
    .replace('\\x9f', 'ş')
    .replace('\\x9e', 'Ş')
    .replace('\\x87', 'ç')
    .replace('\\x80', 'Ç')
    .replace('\\xa7', 'ğ')
    .replace('\\xa6', 'Ğ')
    .replace('\\x98', 'İ')
    .replace('\\x8d', 'ı')
    .split('All User Profile     :')[1:])

for wifiName in wifiNamesList:
    wifiName = wifiName.strip()
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
