"""
Random cipher creator.
"""

import random
import pprint
import os
from pathlib import Path

import cipherTranslate

"""
# Create a random cipher.
usedKeys = []
characters = {}
for i in range(32, 127):
    while True:
        randomChr = random.randint(32, 5000)
        if randomChr not in usedKeys:
            if chr(randomChr).isprintable():
                characters[i] = randomChr
                usedKeys.append(randomChr)
                break

with open('cipherTranslate.py', 'w', encoding='UTF-8') as cipher:
    cipher.write('characters = ' + pprint.pformat(characters))
"""

myText = "youcantenter55"

ciphered = myText.translate(cipherTranslate.characters)

print(ciphered)

reverseCipher = {v: k for k, v in cipherTranslate.characters.items()}

reverseCiphered = ciphered.translate(reverseCipher)

print(reverseCiphered)
