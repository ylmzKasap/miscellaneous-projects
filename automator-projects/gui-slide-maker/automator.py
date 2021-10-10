import pyautogui, time, os, sys, copy, re, pprint
from pathlib import Path

currentProjects = os.listdir(f'{os.getcwd()}\\Projects')
forbiddenCharacters = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

def correctProjectName(projectName):
    nameError = 0
    try:
        while True:
            if projectName == "" or projectName.isspace():
                projectName = pyautogui.prompt(
                    "Projenizin bir adı olmalı."
                    "Hiçbir şey yazmadınız. Tekrar bir isim girin."
                    )
                continue
            for i in forbiddenCharacters:
                if i in projectName:
                    projectName = pyautogui.prompt(
                        f"Proje adı '{i}' içeremez. Yeni bir isim girin."
                        )
                    nameError = 1
                    break
            if nameError == 1:
                nameError = 0
                continue
            break
    except AttributeError:
        print(
            "\nGeçerli bir proje ismi girmediğiniz için "
            "program sonlandırıldı."
            )
        input()
        sys.exit()


if len(currentProjects) == 0:
    projectName = pyautogui.prompt(
        "Yeni bir projeye başlamak için bir proje adı girin."
        )
    correctProjectName(projectName)
elif len(currentProjects) == 1:
    projectName = currentProjects[0]
else:
    projectName = pyautogui.prompt(
        "Hangi projeden devam etmek istiyorsunuz? "
        "\n\nMevcut projeler:\n"
        + ('\n').join(currentProjects)
        + "\n\nFarklı bir isim girerek yeni bir projeye başlayabilirsiniz."
        )
    correctProjectName(projectName)

saveName = 'savedProject.py'
allDirections = []  # List of directions for all episodes, to be saved later
allEpisodeNames = []  # List of names for all episodes, to be saved later

try:
    projectPath = Path.cwd() / 'Projects' / projectName
except TypeError:
    print('\nGeçerli bir proje ismi girmediğiniz için program sonlandırıldı.')
    input()
    sys.exit()

projectPath2 = f'{os.getcwd()}\\Projects\\{projectName}'

# --- For specific projects, delete or change when needed --- Required to create a variable dictionary
imageDestination = f'{os.getcwd()}\\Files\\Image Files'
soundDestination = f'{os.getcwd()}\\Files\\Sound Files'

directoryError = 0
variableDict = {}
variableSymbol = 'v'

try:
    imageDestinationContents = os.listdir(imageDestination)
    soundDestinationContents = os.listdir(soundDestination)
    words = []
    getTillDot = re.compile(r'[^.]+')

    for i in imageDestinationContents:
        words.append(getTillDot.search(i).group())

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

except FileNotFoundError:
    directoryError = 1

# --- For specific projects, delete or change when needed ---


if not projectPath.exists():
    os.makedirs(projectPath)

originalScreenSize = (pyautogui.size().width, pyautogui.size().height)
directions = [] # List of directions for CURRENT episode
turn = 1 # Direction number for the current episode
info = 0 # The number of times command info is provided
episode = 1 # Episode number
error = 0 # Switches to "1" if there is an error. Prevents os.system('cls').
actionDuration = 0.65 # Action time for each direction

if (projectPath / saveName).exists():
    sys.path.insert(1, projectPath2)
    import savedProject
    allDirections = savedProject.allDirectionsSave
    allEpisodeNames = savedProject.allEpisodeNamesSave
    episode = len(allDirections)+1

directionsRegex = re.compile(r'-.*')
episodesRegex = re.compile(r'\..*')

keyToText = {
    '.': '-normal_click',
    '..': '-click_color',
    'c': '-move_cursor',
    'cc': '-moveCursor_color',
    'd': '-double_click',
    'dd': '-doubleClick_color',
    'r': '-right_click',
    'rr': '-rightClick_color',
    'm': '-middle_click',
    'mm': '-middleClick_color',
    'dt': '-drag_to',
    'dtt': '-dragTo_color',
    'su': '-scrollUp',
    'sd': '-scrollDown',
    }

keyToTextImage = {
    '.': '-clickImage',
    'c': '-moveCursorImage',
    'd': '-doubleClickImage',
    'r': '-rightClickImage',
    'dt': '-dragToImage'
    }

hotkeys = {
    'copy': ['-copy', 'ctrl+C'],
    'paste': ['-paste', 'ctrl+V'],
    'sAll': ['-selectAll', 'ctrl+A'],
    'cut': ['-cutSelected', 'ctrl+X'],
    'undo': ['-undo', 'ctrl+Z'],
    'redo': ['-redo', 'ctrl+Y'],
    'save': ['-saveIt', 'ctrl+S'],
    'save as': ['-saveAs', 'ctrl+shift+S'],
    'exit': ['-exitIt', 'alt+f4']
    }

keyboard = {
    'esc': ['-pressEscape', 'escape'],
    'del': ['-pressDelete', 'delete'],
    'backspace': ['-pressBackspace', 'backspace'],
    'enter': ['-pressEnter', 'enter'],
    'tab': ['-pressTab', 'tab'],
    'up': ['-pressUp', 'up arrow'],
    'down': ['-pressDown', 'down arrow'],
    'right': ['-pressRight', 'right arrow'],
    'left': ['-pressLeft', 'left arrow'],
    'home': ['-pressHome', 'home'],
    'end': ['-pressEnd', 'end']
    }

allAssignments = {
    '.': 'Düz tık',
    '..': 'Renk tutuyorsa düz tık',
    'd': 'Çift tıkla',
    'dd': 'Renk tutuyorsa çift tıkla',
    'r': 'Sağ tıkla',
    'rr': 'Renk tutuyorsa sağ tıkla',
    'm': 'Orta tık',
    'mm': 'Renk tutuyorsa orta tıkla',
    'v': 'Değer ata',
    'k': 'Yazı yazma ata',
    'hot': 'Tuş kombinasyonu ata',
    'p': 'Basılacak bir tuş ata',
    'max': 'Pencereyi büyütme ata',
    'w': 'Bekleme ata',
    'c': 'Fareyi hareket ettir',
    'cc': 'Renk tutuyorsa fareyi hareket ettir',
    'dt': 'Koordinata sürükle',
    'dtt': 'Renk tutuyorsa koordinata sürükle',
    'su': 'Yukarı kaydır',
    'sd': 'Aşağı kaydır',
    'h': 'Fareyi basılı tutma ata',
    'hc': 'Bir tuşa basarak tıkla',
    'i': 'Resim tanıma işlemini başlat',
    }

helpMenu = {
    'epi': 'Bölümleri listele',
    'name': 'Bölümün ismini değiştir',
    'save': 'Bölümü kaydet',
    'go': 'Belirli bir bölüme git',
    'copy': 'Bir bölümün içeriğini başka bir bölüme kopyala',
    'del': 'Belirli bir bölümü sil',
    'insep': 'Belirli bir bölümden sonra yeni bir bölüm ekle',
    'runep': 'Belirli bir bölümden itibaren tüm talimatları oynat',
    'run': 'Mevcut bölümün talimatlarını oynat',
    'rep': 'Belirli bir talimatı başka bir talimatla değiştir',
    'ins': 'Belirli bir talimattan sonra yeni bir talimat ata',
    '-': 'Son talimatı sil',
    '--': 'Belirli bir talimatı sil',
    'z': 'Fareyi son adımda bulunduğu yere götür',
    'zz': 'Fareyi iki adım önce bulunduğu yere götür',
    'zzz': 'Fareyi ekranda özel bir yere götür',
    'qq': 'Çıkış'
    }

def keyToAction(key, change, insertion):
    global turn
    currentPos = pyautogui.position()
    if insertion == 1:
        directions.insert(turn-1, [])
        directions[turn-1] = ([f'{turn}{keyToText[key]}'])
        directions[turn-1].append(list((currentPos.x, currentPos.y)))
        while True:
            try:
                directions[turn-1].append(pyautogui.pixel(currentPos.x, currentPos.y))
                break
            except OSError:
                time.sleep(0.2)
                continue
        for index, i in enumerate(directions):
            directions[index][0] = f'{index+1}{directionsRegex.search(i[0]).group()}'
        turn = len(directions) + 1
        insertion = 0
        return change, insertion
    if change == 0:
        directions.append([])
    directions[turn-1] = ([f'{turn}{keyToText[key]}'])
    directions[turn-1].append(list((currentPos.x, currentPos.y)))
    while True:
        try:
            directions[turn-1].append(pyautogui.pixel(currentPos.x, currentPos.y))
            break
        except OSError:
            time.sleep(0.2)
            continue
    if change == 1:
        change = 0
        turn = len(directions) + 1
        return change, insertion
    turn += 1
    return change, insertion

def keyToImageAction(key, imageName, change, insertion):
    global turn
    if insertion == 1:
        directions.insert(turn-1, [])
        directions[turn-1] = ([f'{turn}{keyToTextImage[key]}'])
        directions[turn-1].append(f'{os.getcwd()}\\Pictures\\{imageName}')
        for index, i in enumerate(directions):
            directions[index][0] = f'{index+1}{directionsRegex.search(i[0]).group()}'
        turn = len(directions) + 1
        insertion = 0
        return change, insertion
    if change == 0:
        directions.append([])
    directions[turn-1] = ([f'{turn}{keyToTextImage[key]}'])
    directions[turn-1].append(f'{os.getcwd()}\\Pictures\\{imageName}')
    if change == 1:
        change = 0
        turn = len(directions) + 1
        return change, insertion
    turn += 1
    return change, insertion

def incorrectColor(point):
    while True:
        try:
            while not pyautogui.pixelMatchesColor(point[1][0], point[1][1], point[2]):
                print(f'\n{point[0]} için renk değerleri uyuşmuyor.')
                print(f'Beklenen değer: {point[2]}')
                print(f'Mevcut değer: {pyautogui.pixel(point[1][0], point[1][1])}')
                time.sleep(4)
                os.system('cls')
            break
        except OSError:
            time.sleep(0.2)
            continue

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

def variableProcessor(variableDictionary):
    if directoryError == 1:
        print('\nDeğişkenlerin toplanacağı dizin bulunamadı. Bu yöntem kullanılamıyor.')
        print(f'\nAranan yollar:\n{imageDestination}\n{soundDestination}')
        input()
        return
    allowedRange = len(list(variableDictionary.keys()))
    numberError, numberErrorMessage = 0, '\nBir sayı girin.'
    rangeError, rangeErrorMessage = 0, f'\nSayı 1 ile {allowedRange} arasında olmalı.'
    if allowedRange == 0:
        print('\nDeğişken sözlüğüne hiçbir değer girmemişsiniz.')
        time.sleep(2)
        return
    while True:
        try:
            os.system('cls')
            if numberError == 1:
                print(numberErrorMessage)
                numberError = 0
            if rangeError == 1:
                print(rangeErrorMessage)
                rangeError = 0
            print('\nBurada kaçıncı değişken kullanılsın?')
            print('Mevcut değişkenler:\n')
            for index, v in enumerate(variableDictionary.values()):
                print(f'{index+1}. {v}')
            variable = input()
            variable = int(variable)
        except ValueError:
            numberError = 1
            continue
        if variable < 1 or variable > allowedRange:
            rangeError = 1
            continue
        break
    variableTranslation = variableSymbol + str(variable)
    return variableTranslation

def runTheEpisode(actions, aTime):
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

changeInPlace = 0
insertionInPlace = 0
firstTime = 0

while True:
    if error == 0:
        os.system('cls')
    error = 0

    if firstTime == 0:
        print(f'\nProje: {projectName}')
        firstTime = 1

    try:
        print(f'\n{allEpisodeNames[episode-1]}\n')
    except IndexError:
        print(f'\n{episode}. Bölüm')

    if len(directions) > 0:
        pprint.pprint(directions)

    dir = input()

    if dir == 'zzz':
        while True:
            print('\nFare x düzleminde hangi koordinata gitsin?')
            x = input()
            print('\nFare y düzleminde hangi koordinata gitsin?')
            y = input()
            try:
                pyautogui.moveTo(x=int(x), y=int(y), duration=1)
            except ValueError:
                os.system('cls')
                print('\nKoordinat olarak sadece sayı girin.\n')
                continue
            os.system('cls')
            print(f'\n{episode}. Bölüm\n')
            if len(directions) > 0:
                pprint.pprint(directions)
            dir = input()
            if dir != 'zzz':
                break
    if dir == 'z':
        try:
            pyautogui.moveTo(directions[-1][1], duration=1)
        except:
            continue
        continue
    if dir == 'zz':
        try:
            pyautogui.moveTo(directions[-2][1], duration=1)
        except:
            continue
        continue

    if dir == 'help':
        os.system('cls')
        print()
        for k, v in helpMenu.items():
            print(f'{k}: {v}')
            error = 1
        print('\nTalimat: Fare veya klavyeye verilen otomasyon görevlerinin her biri.')
        print('\nBölüm: İçinde talimatlar bulunan, \'save\' komutu ile kaydedilen talimatlar dizisi.')
        continue


    if dir == 'epi':
        os.system('cls')
        if len(allEpisodeNames) > 0:
            print('\nAll episodes:')
            print()
            for i in allEpisodeNames:
                print(i)
        else:
            print('\nKayıtlı bir bölüm bulunmuyor.')
        print()
        error = 1
        continue

    abortReplace = 0

    if dir == 'rep':
        if len(directions) == 0:
            print('\nDeğiştirilecek talimat bulunmuyor.')
            time.sleep(2)
            continue
        notFound = 0
        while True:
            os.system('cls')
            if notFound == 1:
                print('\nBöyle bir talimat bulunmuyor.')
                notFound = 0
            print('\nBütün talimatlar:')
            pprint.pprint(directions)
            print('\nHangi talimat değiştirilsin? q iptal eder.')
            allDirectionsForReplacement = []
            for i in range(1, len(directions)+1):
                allDirectionsForReplacement.append(str(i))
            replacedDirection = input()
            if replacedDirection == 'q':
                abortReplace = 1
                break
            if replacedDirection not in allDirectionsForReplacement:
                notFound = 1
                continue
            replacedDirection = int(replacedDirection)
            turn = replacedDirection
            changeInPlace = 1
            break

    if abortReplace == 1:
        continue

    if changeInPlace == 1:
        os.system('cls')
        print(f'\n{directions[replacedDirection-1]} yerine yazılacak olan talimatı girin.')
        dir = input()
        while dir not in list(allAssignments.keys()):
            os.system('cls')
            print('\nBöyle bir talimat bulunmuyor. Mevcut talimatlar:')
            for k, v in allAssignments.items():
                print(f'{k}: {v}')
            dir = input()

    abortInsertion = 0

    if dir == 'ins':
        if len(directions) == 0:
            print('\nArasına iliştirme yapılacak talimat bulunmuyor.')
            time.sleep(2)
            continue
        notFound = 0
        while True:
            os.system('cls')
            if notFound == 1:
                print('\nBöyle bir talimat bulunmuyor.')
                notFound = 0
            print('\nBütün talimatlar:')
            pprint.pprint(directions)
            print('\nKaçıncı talimattan sonra yeni bir talimat eklensin? q iptal eder.')
            allDirectionsForInsertion = []
            for i in range(0, len(directions)+1):
                allDirectionsForInsertion.append(str(i))
            insertionDirection = input()
            if insertionDirection == 'q':
                abortInsertion = 1
                break
            if insertionDirection not in allDirectionsForInsertion:
                notFound = 1
                continue
            insertionDirection = int(insertionDirection)
            turn = insertionDirection+1
            insertionInPlace = 1
            break

    if abortInsertion == 1:
        continue

    if insertionInPlace == 1:
        os.system('cls')
        if insertionDirection == 0:
            print(f'\n{directions[insertionDirection]} öncesinde yazılacak olan talimatı girin.')
            dir = input()
            while dir not in list(allAssignments.keys()):
                os.system('cls')
                print('\nBöyle bir talimat bulunmuyor. Mevcut talimatlar:')
                for k, v in allAssignments.items():
                    print(f'{k}: {v}')
                dir = input()
        else:
            print(f'\n{directions[insertionDirection-1]} ardından yazılacak olan talimatı girin.')
            dir = input()
            while dir not in list(allAssignments.keys()):
                os.system('cls')
                print('\nBöyle bir talimat bulunmuyor. Mevcut talimatlar:')
                for k, v in allAssignments.items():
                    print(f'{k}: {v}')
                dir = input()

    if dir == 'name':
        print('\nBölümün ismi ne ile değiştirilsin?')
        episodeName = input()
        try:
            allEpisodeNames[episode-1] = f'{str(episode)}. {episodeName}'
        except IndexError:
            allEpisodeNames.append(f'{str(episode)}. {episodeName}')
        continue

    if dir == 'run':
        print('\n3 saniye içinde bölüm çalışmaya başlayacak.')
        time.sleep(3)
        try:
            runTheEpisode(directions, actionDuration)
        except pyautogui.FailSafeException:
            pass
        continue

    if dir == 'runep':
        if len(allDirections) == 0:
            os.system('cls')
            print('\nOynatılacak bölüm bulunmuyor.')
            error = 1
            continue
        os.system('cls')
        print('\nAll episodes:')
        print()
        previousEpisodes = []
        for i in allEpisodeNames:
            print(i)
        print(f'\nKaçıncı bölümden itibaren oynatılsın? Geride toplam {episode-1} bölüm var.\n')
        print('\'q\' iptal eder.')
        for i in range(1, episode):
            previousEpisodes.append(str(i))
        runEpisode = input()
        if runEpisode == 'q':
            continue
        while runEpisode not in previousEpisodes:
            os.system('cls')
            print('\nAll episodes:')
            print()
            for i in allEpisodeNames:
                print(i)
            print(f'\nBöyle bir bölüm yok. Geride {episode-1} bölüm mevcut.')
            print('Kaçıncı bölümden itibaren oynatılsın?')
            runEpisode = input()
        runEpisode = int(runEpisode)
        print(f'\n3 saniye içinde {runEpisode}. bölümden itibaren oynatılmaya başlanacak.')
        time.sleep(3)
        try:
            for permittedDirections in allDirections[runEpisode-1:episode]:
                runTheEpisode(permittedDirections, actionDuration)
            try:
                if directions != allDirections[episode-1]:
                    runTheEpisode(directions, actionDuration)
            except IndexError:
                pass
        except pyautogui.FailSafeException:
            pass
        continue

    if dir == 'save':
        saveFile = open(projectPath / 'savedProject.py', 'w', encoding="utf8")
        saveFile.write('\nscreenSize = ' + pprint.pformat(originalScreenSize) + '\n')
        try:
            allDirections[episode-1] = copy.deepcopy(directions)
        except IndexError:
            allDirections.append(copy.deepcopy(directions))
        saveFile.write('\nallDirectionsSave = ' + pprint.pformat(allDirections))
        directions = []
        turn = 1
        try:
            episodeName = allEpisodeNames[episode-1]
        except IndexError:
            episodeName = f'{episode}. Bölüm'
        try:
            allEpisodeNames[episode-1] = episodeName
        except IndexError:
            allEpisodeNames.append(episodeName)
        saveFile.write('\n\nallEpisodeNamesSave = ' + pprint.pformat(allEpisodeNames))
        episode = len(allDirections)+1
        saveFile.close()
        continue

    if dir == 'go':
        if len(allEpisodeNames)>len(allDirections):
            del allEpisodeNames[-1]
        if len(allDirections) == 0:
            os.system('cls')
            print('\nGidilecek bölüm bulunmuyor.')
            error = 1
            continue
        os.system('cls')
        print('\nAll episodes:')
        print()
        for i in allEpisodeNames:
            print(i)
        print(f'\n\nKaçıncı bölüme gidilsin? Toplam {len(allDirections)} bölüm var.\n')
        print('Mevcut bölüm kaydedilmediyse silinecektir. \'q\' iptal eder.')
        currentEpisodes = []
        for i in range(1, len(allDirections)+1):
            currentEpisodes.append(str(i))
        goEpisode = input()
        if goEpisode == 'q':
            continue
        while goEpisode not in currentEpisodes:
            os.system('cls')
            print('\nAll episodes:')
            print()
            for i in allEpisodeNames:
                print(i)
            print(f'\nBöyle bir bölüm yok. Toplam {len(allDirections)} bölüm mevcut.')
            print('Kaçıncı bölüme gidilsin?')
            goEpisode = input()
        episode = int(goEpisode)
        directions = copy.deepcopy(allDirections[episode-1])
        turn = len(directions)+1
        continue

    if dir == 'copy':
        os.system('cls')
        print('\nAll episodes:')
        print()
        for i in allEpisodeNames:
            print(i)
        print(f'\n\nKaçıncı bölümün içeriği bu bölüme kopyalansın? Toplam {len(allDirections)} bölüm var.\n')
        copyEpisode = input()
        if copyEpisode == 'q':
            continue
        currentEpisodes = []
        for i in range(1, len(allDirections)+1):
            currentEpisodes.append(str(i))
        while copyEpisode not in currentEpisodes:
            os.system('cls')
            print('\nAll episodes:')
            print()
            for i in allEpisodeNames:
                print(i)
            print(f'\nBöyle bir bölüm yok. Toplam {len(allDirections)} bölüm mevcut.')
            print('Kaçıncı bölüm buraya kopyalansın?')
            copyEpisode = input()
        copyEpisode = int(copyEpisode)
        directions = copy.deepcopy(allDirections[copyEpisode-1])
        turn = len(directions)+1
        continue

    if dir == 'del':
        if len(allEpisodeNames)>len(allDirections): # Bölüm kaydedilmediyse ekstra bölüm ismini sil
            del allEpisodeNames[-1]
        if len(allDirections) == 0:
            os.system('cls')
            print('\nSilinecek bölüm bulunmuyor.')
            error = 1
            continue
        os.system('cls')
        print('\nAll episodes:')
        print()
        for i in allEpisodeNames:
            print(i)
        print(f'\n\nKaçıncı bölüm silinsin? Toplam {len(allDirections)} bölüm var.\n')
        print('Mevcut bölüm kaydedilmediyse unutulacaktır. \'q\' iptal eder.')
        currentEpisodes = []
        for i in range(1, len(allDirections)+1):
            currentEpisodes.append(str(i))
        delEpisode = input()
        if delEpisode == 'q':
            continue
        while delEpisode not in currentEpisodes:
            os.system('cls')
            print('\nAll episodes:')
            print()
            for i in allEpisodeNames:
                print(i)
            print(f'\nBöyle bir bölüm yok. Toplam {len(allDirections)} bölüm mevcut.')
            print('Kaçıncı bölüm silinsin?')
            delEpisode = input()
        delEpisode = int(delEpisode)
        del allDirections[delEpisode-1]
        del allEpisodeNames[delEpisode-1]
        for index, i in enumerate(allEpisodeNames):
            allEpisodeNames[index] = f'{index+1}{episodesRegex.search(i).group()}'
        try:
            directions = copy.deepcopy(allDirections[len(allDirections)-1])
            episode = len(allDirections)
        except IndexError:
            directions = []
            episode = 1
        turn = len(directions)+1
        continue

    if dir == 'insep':
        if len(allDirections) == 0:
            print('\nArasına iliştirme yapılacak bölüm bulunmuyor.')
            time.sleep(2)
            continue
        notFound = 0
        while True:
            os.system('cls')
            if notFound == 1:
                print('\nBöyle bir bölüm bulunmuyor.')
                notFound = 0
            print('\nBütün bölümler:')
            for i in allEpisodeNames:
                print(i)
            print('\nKaçıncı bölümden sonra yeni bir bölüm eklensin?\
            \nKaydedilmemiş bölümün içeriği silinecektir. q iptal eder.')
            allEpisodesForInsertion = []
            for i in range(0, len(allDirections)+1):
                allEpisodesForInsertion.append(str(i))
            insertionDirection = input()
            if insertionDirection == 'q':
                abortInsertion = 1
                break
            if insertionDirection not in allEpisodesForInsertion:
                notFound = 1
                continue
            insertionDirection = int(insertionDirection)
            allDirections.insert(insertionDirection, [])
            allEpisodeNames.insert(insertionDirection, [])
            allEpisodeNames[insertionDirection] = '999. Bölüm'
            for index, i in enumerate(allEpisodeNames):
                allEpisodeNames[index] = f'{index+1}{episodesRegex.search(i).group()}'
            directions = []
            episode = insertionDirection+1
            turn = len(directions)+1
            break
        continue

    if abortInsertion == 1:
        continue

    if dir == 'v':
        os.system('cls')
        variableToBeWritten = variableProcessor(variableDict)
        if variableToBeWritten == None:
            if changeInPlace == 1:
                turn = len(directions) + 1
                changeInPlace = 0
            if insertionInPlace == 1:
                turn = len(directions) + 1
                insertionInPlaceInPlace = 0
            continue
        if insertionInPlace == 1:
            directions.insert(turn-1, [])
            directions[turn-1] = ([f'{turn}-writeVariable'])
            directions[turn-1].append(variableToBeWritten)
            for index, i in enumerate(directions):
                directions[index][0] = f'{index+1}{directionsRegex.search(i[0]).group()}'
            turn = len(directions) + 1
            insertionInPlace = 0
            continue
        if changeInPlace == 0:
            directions.append([])
        directions[turn-1] = ([f'{turn}-writeVariable'])
        directions[turn-1].append(variableToBeWritten)
        if changeInPlace == 1:
            turn = len(directions) + 1
            changeInPlace = 0
            continue
        turn += 1
        continue

    elif dir == 'k':
        os.system('cls')
        print('\nKlavye ile ne yazılmasını istersiniz?')
        writeIt = input()
        if insertionInPlace == 1:
            directions.insert(turn-1, [])
            directions[turn-1] = ([f'{turn}-writeText'])
            directions[turn-1].append(writeIt)
            for index, i in enumerate(directions):
                directions[index][0] = f'{index+1}{directionsRegex.search(i[0]).group()}'
            turn = len(directions) + 1
            insertionInPlace = 0
            continue
        if changeInPlace == 0:
            directions.append([])
        directions[turn-1] = ([f'{turn}-writeText'])
        directions[turn-1].append(writeIt)
        if changeInPlace == 1:
            turn = len(directions) + 1
            changeInPlace = 0
            continue
        turn += 1
        continue

    elif dir == 'hot':
        os.system('cls')
        print('\nHangi tuş kombinasyonuna basılsın?')
        print('\nMevcut tuşlar:')
        for hotkey in list(hotkeys.keys()):
            print(f'{hotkey}: {hotkeys[hotkey][1]}')
        hotkeyDecision = input()
        while hotkeyDecision not in list(hotkeys.keys()):
            os.system('cls')
            print(f'\n{hotkeyDecision} adında bir tuş kombinasyonu mevcut değil.')
            print('\nMüsait tuşlar:')
            for hotkey in list(hotkeys.keys()):
                print(f'{hotkey}: {hotkeys[hotkey][1]}')
            hotkeyDecision = input()
        if insertionInPlace == 1:
            directions.insert(turn-1, [])
            directions[turn-1] = ([f'{turn}-hotkey'])
            directions[turn-1].append(hotkeyDecision)
            for index, i in enumerate(directions):
                directions[index][0] = f'{index+1}{directionsRegex.search(i[0]).group()}'
            turn = len(directions) + 1
            insertionInPlace = 0
            continue
        if changeInPlace == 0:
            directions.append([])
        directions[turn-1] = ([f'{turn}-hotkey'])
        directions[turn-1].append(hotkeyDecision)
        if changeInPlace == 1:
            turn = len(directions) + 1
            changeInPlace = 0
            continue
        turn += 1
        continue

    elif dir == 'hc':
        holdKeys = ['ctrl', 'shift', 'alt']
        currentPos = pyautogui.position()
        print('\nBuraya tıklamadan önce hangi tuşa basılsın?')
        print('\nMevcut tuşlar:')
        for i in holdKeys:
            print(i)
        holdKey = input()
        while holdKey not in holdKeys:
            os.system('cls')
            print('\nBöyle bir tuş mevcut değil')
            print('\nMevcut tuşlar:\n')
            for i in holdKeys:
                print(i)
            holdKey = input()
        if insertionInPlace == 1:
            directions.insert(turn-1, [])
            directions[turn-1] = ([f'{turn}-holdClick'])
            directions[turn-1].append(holdKey)
            directions[turn-1].append(list((currentPos.x, currentPos.y)))
            for index, i in enumerate(directions):
                directions[index][0] = f'{index+1}{directionsRegex.search(i[0]).group()}'
            turn = len(directions) + 1
            insertionInPlace = 0
            continue
        if changeInPlace == 0:
            directions.append([])
        directions[turn-1] = ([f'{turn}-holdClick'])
        directions[turn-1].append(holdKey)
        directions[turn-1].append(list((currentPos.x, currentPos.y)))
        if changeInPlace == 1:
            turn = len(directions) + 1
            changeInPlace = 0
            continue
        turn += 1
        continue

    elif dir == 'p':
        os.system('cls')
        print('\nHangi tuşa basılsın?')
        print('\nMevcut tuşlar:')
        for key in list(keyboard.keys()):
            print(f'{key}: {keyboard[key][1]}')
        keyDecision = input()
        while keyDecision not in list(keyboard.keys()):
            os.system('cls')
            print(f'\n{keyDecision} adında bir tuş mevcut değil.')
            print('\nMüsait tuşlar:')
            for key in list(keyboard.keys()):
                print(f'{key}: {keyboard[key][1]}')
            keyDecision = input()
        if insertionInPlace == 1:
            directions.insert(turn-1, [])
            directions[turn-1] = ([f'{turn}-pressKey'])
            directions[turn-1].append(keyDecision)
            for index, i in enumerate(directions):
                directions[index][0] = f'{index+1}{directionsRegex.search(i[0]).group()}'
            turn = len(directions) + 1
            insertionInPlace = 0
            continue
        if changeInPlace == 0:
            directions.append([])
        directions[turn-1] = ([f'{turn}-pressKey'])
        directions[turn-1].append(keyDecision)
        if changeInPlace == 1:
            turn = len(directions) + 1
            changeInPlace = 0
            continue
        turn += 1
        continue

    elif dir == 'maxW':
        print('3 saniye içinde aktif pencere büyütülecek.')
        time.sleep(3)
        activeWindow = pyautogui.getActiveWindow()
        activeWindow.maximize()
        continue
    elif dir == 'max':
        if insertionInPlace == 1:
            directions.insert(turn-1, [])
            directions[turn-1] = ([f'{turn}-maximizeWindow'])
            for index, i in enumerate(directions):
                directions[index][0] = f'{index+1}{directionsRegex.search(i[0]).group()}'
            turn = len(directions) + 1
            insertionInPlace = 0
            continue
        if changeInPlace == 0:
            directions.append([])
        directions[turn-1] = ([f'{turn}-maximizeWindow'])
        if changeInPlace == 1:
            turn = len(directions) + 1
            changeInPlace = 0
            continue
        turn += 1
        continue

    elif dir == 'h':
        os.system('cls')
        print('\nFareye ne kadar süre basılı tutulsun?')
        holdTime = input()
        while True:
            try:
                holdTime = int(holdTime)
                break
            except ValueError:
                os.system('cls')
                print('\nBir sayı girin.')
                holdTime = input()
        if insertionInPlace == 1:
            directions.insert(turn-1, [])
            directions[turn-1] = ([f'{turn}-holdMouse'])
            directions[turn-1].append(holdTime)
            for index, i in enumerate(directions):
                directions[index][0] = f'{index+1}{directionsRegex.search(i[0]).group()}'
            turn = len(directions) + 1
            insertionInPlace = 0
            continue
        if changeInPlace == 0:
            directions.append([])
        directions[turn-1] = ([f'{turn}-holdMouse'])
        directions[turn-1].append(holdTime)
        if changeInPlace == 1:
            turn = len(directions) + 1
            changeInPlace = 0
            continue
        turn += 1
        continue

    elif dir == 'w':
        os.system('cls')
        print('\nKaç saniye beklensin?')
        waiting = input()
        while True:
            try:
                waiting = int(waiting)
                break
            except ValueError:
                os.system('cls')
                print('\nBir sayı girin.')
                waiting = input()
        if insertionInPlace == 1:
            directions.insert(turn-1, [])
            directions[turn-1] = ([f'{turn}-wait'])
            directions[turn-1].append(waiting)
            for index, i in enumerate(directions):
                directions[index][0] = f'{index+1}{directionsRegex.search(i[0]).group()}'
            turn = len(directions) + 1
            insertionInPlace = 0
            continue
        if changeInPlace == 0:
            directions.append([])
        directions[turn-1] = ([f'{turn}-wait'])
        directions[turn-1].append(waiting)
        if changeInPlace == 1:
            turn = len(directions) + 1
            changeInPlace = 0
            continue
        turn += 1
        continue

    elif dir in list(keyToText.keys()):
        changeInPlace, insertionInPlace = keyToAction(dir, changeInPlace, insertionInPlace)
        continue

    elif dir == 'i':
        os.system('cls')
        print('\nEkranda bulunmasını istediğiniz resmin ekran görüntüsünü alın.')
        print('Sonrasında resmi, \'Pictures\' klasörüne kaydedin.')
        print('\nBu işlemi tamamlayınca enter\'a basın.')
        input()
        os.system('cls')
        print('\nResim dosyasının ismini uzantısıyla birlikte yazın.')
        ssName = input()
        while True:
            print(f'\nDosyanın ismi "{ssName}" olarak kaydedildi.')
            print('Devam etmek için enter\'a basın.')
            decision = input()
            if decision == '':
                break
            else:
                os.system('cls')
                print('\nResim dosyasının ismini uzantısıyla birlikte yazın.')
                ssName = input()
        os.system('cls')
        print('\nBu resim üzerinde hangi işlem yapılsın?')
        print('\n\'.\': Düz tık\n\'r\': Sağ tık\n\'d\': Çift tık\n\'dt\': Taşı\n\'c\': Fareyi götür.')
        decision = input()
        while not decision in list(keyToTextImage.keys()):
            os.system('cls')
            print('\nBöyle bir komut yok. Mevcut komutlar:')
            print('\n\'.\': Düz tık\n\'r\': Sağ tık\n\'d\': Çift tık\n\'dt\': Taşı\n\'c\': Fareyi götür.')
            decision = input()
        changeInPlace, insertionInPlace = keyToImageAction(decision, ssName, changeInPlace, insertionInPlace)
        continue

    elif dir == 'qq':
        break
    elif dir == '--':
        if len(directions) == 0:
            os.system('cls')
            print('\nSilinecek bir talimat yok.')
            error = 1
            continue
        elif len(directions) == 1:
            turn -= 1
            del directions[-1]
            continue
        else:
            notFound = 0
            abortRemoval = 0
            while True:
                os.system('cls')
                if notFound == 1:
                    print('\nBöyle bir talimat bulunmuyor.')
                    notFound = 0
                print('\nBütün talimatlar:')
                pprint.pprint(directions)
                print('\nHangi talimat silinsin? q iptal eder.')
                allDirectionsForRemoval = []
                for i in range(1, len(directions)+1):
                    allDirectionsForRemoval.append(str(i))
                deletedDirection = input()
                if deletedDirection == 'q':
                    abortRemoval= 1
                    break
                if deletedDirection not in allDirectionsForRemoval:
                    notFound = 1
                    continue
                deletedDirection = int(deletedDirection)
                break
            if abortRemoval == 1:
                abortRemoval = 0
                continue
            del directions[deletedDirection-1]
            for index, i in enumerate(directions):
                directions[index][0] = f'{index+1}{directionsRegex.search(i[0]).group()}'
            turn -= 1
            continue
    elif dir == '-':
        if turn > 1:
            turn -= 1
            del directions[-1]
        continue
    else:
        if info < 50:
            os.system('cls')
            print('\nBöyle bir komut yok. Mevcut komutlar:\n')
            for k, v in allAssignments.items():
                print(f'{k}: {v}')
            info += 1
            error = 1
        elif info >=50:
            os.system('cls')
            print(f'\n{dir} diye bir komut mevcut değil.')
            error = 1

file = open(Path.cwd() / 'zDirections.py', 'w')
file.write('screenSize = ' + pprint.pformat(originalScreenSize) + '\n\n')
file.write('directions = ' + pprint.pformat(directions))
file.close()

print('\nSON')
input()
