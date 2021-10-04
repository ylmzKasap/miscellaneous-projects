"""
A program which displays the biggest files in the computer
base on their size and extensions.
"""

import datetime
import os
import time


def mb_to_byte(megabytes):
    return megabytes * 1048576


startTime = time.time()

mbTresholdForListed = 10
mbTresholdForListed = mb_to_byte(mbTresholdForListed)
extensionsList = []

tresholdForOthers = 75
tresholdForOthers = mb_to_byte(tresholdForOthers)
othersList = []

extensions = ("png", "PNG", "jpg", "jpeg", "mp4", "mkv", "clopkg", "mp3")

print("\nDosyalar aranıyor...")
for folderName, u, filenames in os.walk("C:\\"):
    if "Windows" in folderName:
        continue

    for filename in filenames:
        filePath = folderName + "\\" + filename
        try:
            fileSize = os.path.getsize(filePath)
            if filePath.endswith(extensions):
                if fileSize > mbTresholdForListed:
                    extensionsList.append([filePath, fileSize])
            elif not filePath.endswith(extensions):
                if fileSize > tresholdForOthers:
                    othersList.append([filePath, fileSize])
        except OSError:
            pass

extensions = [
    [pathOfFile, sizeOfFile]
    for pathOfFile, sizeOfFile in sorted(
        extensionsList, reverse=True, key=lambda g: int(g[1])
    )
]

others = [
    [pathOfFile, sizeOfFile]
    for pathOfFile, sizeOfFile in sorted(
        othersList, reverse=True, key=lambda g: int(g[1])
    )
]

os.system("cls")

print("\nBelirli uzantıdaki dosyalar:")
for p, s in extensions:
    print(f"{round(s / 1048576, 2)} MB -> {p}")

print("\nDiğer dosyalar.")
for p, s in others:
    print(f"{round(s / 1048576, 2)} MB -> {p}")

endTime = time.time()
totalSeconds = datetime.timedelta(seconds=(endTime - startTime))

print(f"Time Passed: {str(totalSeconds)}")
print("\n'Q' çıkar")
while True:
    decision = input().lower()
    if decision == "q":
        break
