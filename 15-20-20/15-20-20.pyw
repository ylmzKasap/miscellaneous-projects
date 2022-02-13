"""
A program that warns the users every 12 and 60 minutes
to rest their eyes and take a walk respectively.
"""

from ctypes import Structure, windll, c_uint, sizeof, byref
from pygame import mixer
import time

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0

mixer.init()
current = checkpoint = 0
while True:
    current += 1
    idleTime = get_idle_duration()
    time.sleep(1)
    if current % 720 == 0:
        mixer.music.load('beep.wav')
        mixer.music.play()
        checkpoint = current
    elif current == 3599:
        mixer.music.load('move.wav')
        mixer.music.play()
        current = checkpoint = 0
    while idleTime > 60:
        time.sleep(1)
        idleTime = get_idle_duration()
        if current > checkpoint:
            current -= 1

