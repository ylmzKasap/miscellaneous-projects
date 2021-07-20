# A shut down scheduler for Windows.

import os
import subprocess
import datetime
import re
import sys

dateRegex = re.compile(r"\d\d:\d\d")

while True:
    print("\nEnter a time to schedule a shut down for your PC. | Use 24-hour format -> 5:30 / 17:30")
    print("Enter 'abort' to cancel the previous shut down order.")
    offTime = input()

    # Cancel previous shutdown order
    if offTime == "abort":
        try:
            os.system('cls')
            print()
            subprocess.check_output(['shutdown', '-a'])
        except subprocess.CalledProcessError:
            continue
        os.system("cls")
        print('\nPrevious shut down order is cancelled.')
        input()

    # Incorrect input
    if dateRegex.search(offTime) is None:
        os.system("cls")
        print("\nEnter the time as in the example below.")
        continue

    # Parse time out of input
    try:
        parsedOffTime = datetime.datetime.strptime(offTime, "%H:%M")
    except ValueError:
        os.system('cls')
        print('\nEnter a valid time.')
        continue
    cTime = datetime.datetime.now()

    shutdownTime = datetime.datetime(
        cTime.year, cTime.month, cTime.day, parsedOffTime.hour, parsedOffTime.minute, 0
    )
    shutdownDelta = shutdownTime - cTime
    shutdownSeconds = shutdownDelta.seconds

    if shutdownSeconds < 60:
        shutdownMinutes = (
            str(shutdownSeconds)
            + (' seconds' if int(shutdownSeconds > 1) else ' second'))
    elif shutdownSeconds >= 60:
        shutdownMinutes = (
            str(round(shutdownSeconds / 60, 1))
            + (' minutes' if shutdownSeconds // 60 > 1 else ' minute'))

    # Schedule it for tomorrow if the time has passed.
    if shutdownDelta.days == -1:
        shutdownTime = datetime.datetime(
            cTime.year, cTime.month, (cTime.day + 1), parsedOffTime.hour, parsedOffTime.minute, 0
        )

    # Execute shutdown order
    try:
        os.system('cls')
        print()
        subprocess.check_output(
            ["shutdown", "-s", "-t", str(shutdownSeconds).rjust(4, "0")],
            shell=True
        )
        print(
            f'The computer will be shut down at {offTime}'
            f' | '
            f'{shutdownTime.day}.{shutdownTime.month}.{shutdownTime.year}'
            f' | '
            f'{shutdownMinutes} left.')
        input()
    except subprocess.CalledProcessError:
        print('\nPlease cancel the previous shut down order first.')
        input()
        sys.exit()
    break
