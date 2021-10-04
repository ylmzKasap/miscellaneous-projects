import openpyxl, traceback, sys, os, shutil
from pathlib import Path

picturePath = 'C:\\Users\\HAL9000\\Desktop\\School\\Materials\\Pictures\\'
soundPath = 'C:\\Users\\HAL9000\\Desktop\\School\\Materials\\Pronunciation Bank\\'
imageDestination = f'{os.getcwd()}\\Files\\Image Files'
soundDestination = f'{os.getcwd()}\\Files\\Sound Files'
workbookName = 'slideWords.xlsx'

if not Path(imageDestination).exists():
    os.makedirs(imageDestination)

if not Path(soundDestination).exists():
    os.makedirs(soundDestination)

try:
    wb = openpyxl.load_workbook('slideWords.xlsx')
    sheet = wb.active
except FileNotFoundError:
    print('\'slideWords.xlsx\'\' isimli dosya, programla aynı klasörde olmalı.')
    input()
    sys.exit()

allColumns = list(sheet.columns)
words = []

for column in allColumns:
    for index, row in enumerate(column):
        if row.value != None:
            words.append(row.value)

imagesNotFound = []
soundsNotFound = []

for foldername, subfolder, filenames in os.walk(picturePath):
    for word in words:
        for filename in filenames:
            if f'{word}.jpg' == filename or f'{word}.png' == filename or f'{word}.jpeg' == filename:
                shutil.copy(foldername + '\\' + filename, imageDestination)
                break

for foldername, subfolder, filenames in os.walk(soundPath):
    for word in words:
        for filename in filenames:
            if f'{word}.wav' == filename:
                shutil.copy(foldername + '\\' + filename, soundDestination)
                break

imageDestinationContents = os.listdir(imageDestination)
soundDestinationContents = os.listdir(soundDestination)

for word in words:
    existing = 0
    for i in imageDestinationContents:
        if word in i:
            existing = 1
    if existing == 0:
        imagesNotFound.append(word)

for word in words:
    existing = 0
    for i in soundDestinationContents:
        if word in i:
            existing = 1
    if existing == 0:
        soundsNotFound.append(word)

if len(imagesNotFound) > 0:
    print('\nBazı kelimeler için resim bulunamadı:')
    for i in imagesNotFound:
        print(i)

if len(imagesNotFound) > 0:
    print('\nBazı kelimeler için ses bulunamadı:')
    for i in soundsNotFound:
        print(i)


