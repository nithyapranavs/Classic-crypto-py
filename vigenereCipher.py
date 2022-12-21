# Vigenere cipher
# Encryption and Decryption

import random

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def keyGen(n):
    #function to generate key
    key = ''
    for i in range(n):
        key += random.choice(list(letters))
    return key

def translate(key, message, mode):
    #function for encryption and decryption
    translated = []
    keyIndex = 0
    key = key.upper()

    for symbol in message:
        num = letters.find(symbol.upper())
        if num != -1: # symbol present in letters
            if mode == 'encrypt':
                num += letters.find(key[keyIndex])
            elif mode == 'decrypt':
                num -= letters.find(key[keyIndex])

            num = num % len(letters)

            #adding the text to CT/PT based on it's case
            if symbol.isupper():
                translated.append(letters[num])
            elif symbol.islower():
                translated.append(letters[num].lower())

            #changing key index
            keyIndex = (keyIndex + 1) % len(key)

        else:
            translated.append(symbol)

    translatedText = ''.join(translated)
    return translatedText

def encrypt(key, message):
    return translate(key, message, "encrypt")

def decrypt(key, message):
    return translate(key, message, "decrypt")
