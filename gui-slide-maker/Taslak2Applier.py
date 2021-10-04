import time, random, sys, os, traceback, shutil, subprocess
from pathlib import Path

try:
    import pyautogui
except ModuleNotFoundError:
    print('\nProgramın çalışması için "pyautogui" adlı modülün yüklü olması gerekiyor.')
    input()
    sys.exit()

try:
    import openpyxl
except ModuleNotFoundError:
    print('\nProgramın çalışması için "openpyxl" adlı modülün yüklü olması gerekiyor.')
    input()
    sys.exit()

# --- Project Information ---
projectName = 'taslak2PP'
projectPath = f'{os.getcwd()}\\Projects\\{projectName}'
saveName = 'savedProject.py'
workbookName = 'slideWords.xlsx'
wordLength = 6  # How many words should be in the excel file
ppName = 'Taslak2'

picturePath = 'C:\\Users\\HAL9000\\Desktop\\School\\Materials\\Pictures'
soundPath = 'C:\\Users\\HAL9000\\Desktop\\School\\Materials\\Pronunciation Bank'
imageDestination = f'{os.getcwd()}\\Files\\Image Files'
soundDestination = f'{os.getcwd()}\\Files\\Sound Files'
templatePath = f'{os.getcwd()}\\Files\\Templates'

PPPath = 'C:/Program Files (x86)/Microsoft Office/root/Office16/POWERPNT.exe'
variableSymbol = 'v'

# --- Create Missing Files ---
if not Path(imageDestination).exists():
    os.makedirs(imageDestination)

if not Path(soundDestination).exists():
    os.makedirs(soundDestination)

if not Path(soundDestination).exists():
    os.makedirs(templatePath)

# --- Load Necessary Files ---
try:
    wb = openpyxl.load_workbook(workbookName)
    sheet = wb.active
except FileNotFoundError:
    print(f'\'{workbookName}\'\' isimli dosya, programla aynı klasörde olmalı.')
    input()
    sys.exit()

try:
    sys.path.insert(1, projectPath)
    import savedProject
    allDirections = savedProject.allDirectionsSave
    allEpisodeNames = savedProject.allEpisodeNamesSave
except ModuleNotFoundError:
    print(f'\n"{saveName}" isimli, talimatların bulunduğu dosya kayıtlı projeler içinde olmalı.')
    input()
    sys.exit()

# --- Screen Size Match ---
originalScreenSize = savedProject.screenSize
currentScreenSize = pyautogui.size()
aTime = 0.5

if originalScreenSize != currentScreenSize:
    print('\nOrijinal ekran çözünürlüğü ile mevcut çözünürlük uyuşmuyor.\n')
    print(f'Orijinal çözünürlük: {originalScreenSize[0]}x{originalScreenSize[1]}')
    print(f'Mevcut çözünürlük: {currentScreenSize[0]}x{currentScreenSize[1]}')
    print('\nBu sebeple program düzgün çalışmayabilir. Yine de devam etmek için enter\'a basın.')
    input()

# --- Get Words and Sound Files ---
allColumns = list(sheet.columns)
words = []

for column in allColumns:  # Get words
    for index, row in enumerate(column):
        if row.value != None:
            words.append(row.value)

if len(words) != wordLength:
    pyautogui.alert(f'\nExcel dosyasında toplam {wordLength} kelime olmalı.\n\
    Şu anda {len(words)} kelime var.', 'Kelime sayısı hatası')
    sys.exit()

imagesNotFound = []
soundsNotFound = []

savedWords = []  # To avoid duplicates
savedSounds = []

# --- Delete previous files to avoid mayhem ---

imageDestinationContents = os.listdir(imageDestination)  # Get file contents
soundDestinationContents = os.listdir(soundDestination)

for i in imageDestinationContents:
    os.unlink(Path(imageDestination, i))

for i in soundDestinationContents:
    os.unlink(Path(soundDestination, i))
# --- Delete previous files to avoid mayhem ---

for foldername, subfolder, filenames in os.walk(picturePath):  # Copy pictures
    for word in words:
        for filename in filenames:
            if f'{word}.jpg' == filename or f'{word}.png' == filename or f'{word}.jpeg' == filename or f'{word}.PNG' == filename:
                if word not in savedWords:
                    shutil.copy(foldername + '\\' + filename, imageDestination)
                    savedWords.append(word)

for foldername, subfolder, filenames in os.walk(soundPath):  # Copy sound files
    for word in words:
        for filename in filenames:
            if word not in savedSounds:
                if f'{word}.wav' == filename:
                    shutil.copy(foldername + '\\' + filename, soundDestination)
                    savedSounds.append(word)
                    break

# --- Get new files ---
imageDestinationContents = os.listdir(imageDestination)
soundDestinationContents = os.listdir(soundDestination)

for word in words:  # Detect images not found
    existing = 0
    for i in imageDestinationContents:
        if word in i:
            existing = 1
    if existing == 0:
        imagesNotFound.append(word)

for word in words:   # Detect sounds not found
    existing = 0
    for i in soundDestinationContents:
        if word in i:
            existing = 1
    if existing == 0:
        soundsNotFound.append(word)

missingFiles = 0

if len(imagesNotFound) > 0:
    print('\nBazı kelimeler için resim bulunamadı:')
    missingFiles = 1
    for i in imagesNotFound:
        print(i)
    for i in imageDestinationContents:
        os.unlink(Path(imageDestination, i))

if len(soundsNotFound) > 0:
    missingFiles = 1
    print('\nBazı kelimeler için ses bulunamadı:')
    for i in soundsNotFound:
        print(i)
    for i in soundDestinationContents:
        os.unlink(Path(soundDestination, i))

if missingFiles == 1:  # Quit if there are images or sounds not found
    print('\nGerekli dosyaları indirdikten sonra kaynak dizine atıp tekrar deneyin.')
    input()
    sys.exit()

variableDict = {}
index = 1
words.sort(key=str.lower)
imageDestinationContents.sort(key=str.lower)
soundDestinationContents.sort(key=str.lower)
for i in range(len(imageDestinationContents)):
        variableDict[variableSymbol + str(index)] = words[i]
        index += 1
        variableDict[variableSymbol + str(index)] = imageDestinationContents[i]
        index += 1
        variableDict[variableSymbol + str(index)] = soundDestinationContents[i]
        index += 1

variableDict[variableSymbol + str(len(list(variableDict.keys())) + 1)] = imageDestination
variableDict[variableSymbol + str(len(list(variableDict.keys())) + 1)] = soundDestination

# --- Functions ---
def imageNotFound(wait):
    waitTime = wait
    os.system('cls')
    print('\nResim ekranda bulunamadı.')
    for i in range(waitTime):
        print(f'\n{waitTime} saniye içinde tekrar denenecek.')
        waitTime -= 1
        time.sleep(1)

def fileNotFound(wait, picture):
    waitTime = wait
    os.system('cls')
    print(f'\n{os.path.basename(picture)}, \'Pictures\' klasörünün içinde değil.')
    for i in range(waitTime):
        print(f'\n{waitTime} saniye içinde tekrar denenecek.')
        waitTime -= 1
        time.sleep(1)

try:
    subprocess.Popen([PPPath, templatePath + '\\' + ppName+'.pptx'])
except FileNotFoundError:
    print(f'\n{ppName} isimli slayt taslağı \'Templates\' klasörü içinde bulunamadı.')
    print('\nDevam etmek için slayt dosyasını kendiniz açın ve enter\'a basın.')
    decision = input()
    if decision == '':
        pass
    else:
        sys.exit()

time.sleep(2)
activeSlide = pyautogui.getActiveWindow()
time.sleep(1)
activeSlide.maximize()

print('\n3 saniye içinde program başlayacak.')
time.sleep(3)

# --- Run Project ---
for actions in savedProject.allDirectionsSave:
    for point in actions:
            if '-normal_click' in point[0]:
                pyautogui.click(point[1], duration=aTime)
            elif '-click_color' in point[0]:
                while True:
                    time.sleep(0.2)
                    if pyautogui.pixelMatchesColor(point[1][0], point[1][1], point[2]):
                        pyautogui.click(point[1], duration=aTime)
                        break
                    else:
                        incorrectColor(point)

            elif '-move_cursor' in point[0]:
                pyautogui.moveTo(point[1], duration=aTime)
            elif '-moveCursor_color' in point[0]:
                time.sleep(0.2)
                while True:
                    if pyautogui.pixelMatchesColor(point[1][0], point[1][1], point[2]):
                        pyautogui.moveTo(point[1], duration=aTime)
                        break
                    else:
                        incorrectColor(point)

            elif '-double_click' in point[0]:
                pyautogui.doubleClick(point[1], duration=aTime)
            elif '-doubleClick_color' in point[0]:
                while True:
                    time.sleep(0.2)
                    if pyautogui.pixelMatchesColor(point[1][0], point[1][1], point[2]):
                        pyautogui.doubleClick(point[1], duration=aTime)
                        break
                    else:

                        incorrectColor(point)
            elif '-right_click' in point[0]:
                pyautogui.rightClick(point[1], duration=aTime)
            elif '-rightClick_color' in point[0]:
                while True:
                    time.sleep(0.2)
                    if pyautogui.pixelMatchesColor(point[1][0], point[1][1], point[2]):
                        pyautogui.rightClick(point[1], duration=aTime)
                        break
                    else:
                        incorrectColor(point)

            elif '-middle_click' in point[0]:
                pyautogui.middleClick(point[1], duration=aTime)
            elif '-middleClick_color' in point[0]:
                while True:
                    time.sleep(0.2)
                    if pyautogui.pixelMatchesColor(point[1][0], point[1][1], point[2]):
                        pyautogui.middleClick(point[1], duration=aTime)
                        break
                    else:
                        incorrectColor(point)

            elif '-drag_to' in point[0]:
                time.sleep(0.2)
                pyautogui.dragTo(point[1], duration=aTime)
            elif '-dragTo_color' in point[0]:
                time.sleep(0.2)
                while True:
                    if pyautogui.pixelMatchesColor(point[1][0], point[1][1], point[2]):
                        pyautogui.dragTo(point[1], duration=aTime)
                        break
                    else:
                        incorrectColor(point)

            elif 'scrollUp' in point[0]:
                time.sleep(0.5)
                for i in range(3):
                    pyautogui.scroll(500)
            elif 'scrollDown' in point[0]:
                time.sleep(0.5)
                for i in range(3):
                    pyautogui.scroll(-500)

            elif '-clickImage' in point[0]:
                time.sleep(0.5)
                while True:
                    try:
                        pyautogui.click(point[1], duration=aTime)
                        break
                    except TypeError:
                        imageNotFound(5)
                    except FileNotFoundError:
                        fileNotFound(10, point[1])

            elif '-moveCursorImage' in point[0]:
                time.sleep(0.5)
                while True:
                    try:
                        pyautogui.moveTo(point[1], duration=aTime)
                        break
                    except TypeError:
                        imageNotFound(5)
                    except FileNotFoundError:
                        fileNotFound(10, point[1])

            elif '-doubleClickImage' in point[0]:
                time.sleep(0.5)
                while True:
                    try:
                        pyautogui.doubleClick(point[1], duration=aTime)
                        break
                    except TypeError:
                        imageNotFound(5)
                    except FileNotFoundError:
                        fileNotFound(10, point[1])

            elif '-rightClickImage' in point[0]:
                time.sleep(0.5)
                while True:
                    try:
                        pyautogui.rightClick(point[1], duration=aTime)
                        break
                    except TypeError:
                        imageNotFound(5)
                    except FileNotFoundError:
                        fileNotFound(10, point[1])

            elif '-dragToImage' in point[0]:
                time.sleep(0.5)
                while True:
                    try:
                        pyautogui.dragTo(point[1], duration=aTime)
                        break
                    except TypeError:
                        imageNotFound(5)
                    except FileNotFoundError:
                        fileNotFound(10, point[1])

            elif '-wait' in point[0]:
                time.sleep(point[1])

            elif '-maximizeWindow' in point[0]:
                time.sleep(0.2)
                activeWindow = pyautogui.getActiveWindow()
                activeWindow.maximize()

            elif '-holdMouse' in point[0]:
                pyautogui.mouseDown()
                time.sleep(point[1])
                pyautogui.mouseUp()

            elif '-writeText' in point[0]:
                pyautogui.write(point[1], 0.01)

            elif '-hotkey' in point[0]:
                if point[1] == 'copy':
                    pyautogui.hotkey('ctrl', 'c')
                elif point[1] == 'paste':
                    pyautogui.hotkey('ctrl', 'v')
                elif point[1] == 'sAll':
                    pyautogui.hotkey('ctrl', 'a')
                elif point[1] == 'cut':
                    pyautogui.hotkey('ctrl', 'x')
                elif point[1] == 'undo':
                    pyautogui.hotkey('ctrl', 'z')
                elif point[1] == 'redo':
                    pyautogui.hotkey('ctrl', 'y')
                elif point[1] == 'save':
                    pyautogui.hotkey('ctrl', 's')
                elif point[1] == 'save as':
                    pyautogui.hotkey('ctrl', 'shift', 's')
                elif point[1] == 'exit':
                    pyautogui.hotkey('alt', 'f4')

            elif '-pressKey' in point[0]:
                time.sleep(0.2)
                if point[1] == 'esc':
                    pyautogui.press('esc')
                elif point[1] == 'del':
                    pyautogui.press('delete')
                elif point[1] == 'enter':
                    pyautogui.press('enter')
                elif point[1] == 'tab':
                    pyautogui.press('tab')
                elif point[1] == 'up':
                    pyautogui.press('up')
                elif point[1] == 'down':
                    pyautogui.press('down')
                elif point[1] == 'right':
                    pyautogui.press('right')
                elif point[1] == 'left':
                    pyautogui.press('left')
                elif point[1] == 'home':
                    pyautogui.press('home')
                elif point[1] == 'end':
                    pyautogui.press('end')
                elif point[1] == 'backspace':
                    pyautogui.press('backspace')

            elif '-writeVariable' in point[0]:
                pyautogui.write(variableDict[point[1]], 0.01)

            elif '-holdClick' in point[0]:
                time.sleep(0.2)
                pyautogui.keyDown(point[1])
                pyautogui.click(point[2], duration = aTime)
                pyautogui.keyUp(point[1])
