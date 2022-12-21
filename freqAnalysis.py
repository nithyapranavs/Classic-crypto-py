englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33,
                     'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41,
                     'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98,
                     'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}

ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def getLetterCount(message):
    '''Returns dictionary with how many time the
    letter has appeared'''
    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0,
                   'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0,
                   'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0,
                   'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

    for letter in message.upper():
        if letter in LETTERS:
            letterCount[letter] += 1

    return letterCount

def getItemAtIndexZero(x):
    return x[0]

def getFrequencyOrder(message):
    '''Returns a string of letters arranged in order of
    most frequently occuring in the message'''

    letterToFreq = getLetterCount(message)
    #key = letter , value = freq

    freqToLetter = {}
    #key = freq, value = [letter1, letter2]

    for letter in LETTERS:
        if letterToFreq[letter] not in freqToLetter:
            freqToLetter[letterToFreq[letter]] = [letter]
        else:
            freqToLetter[letterToFreq[letter]].append(letter)

    #loop changes the letters list to string
    #eg: val = ['a','b'] -> 'ab'
    for freq in freqToLetter:
        freqToLetter[freq].sort(key = ETAOIN.find, reverse = True)
        freqToLetter[freq] = ''.join(freqToLetter[freq])

    #dict to list of tubles
    #eg: [(1,'ab'),(2,'c')]
    freqPairs = list(freqToLetter.items())
    freqPairs.sort(key = getItemAtIndexZero, reverse = True)

    freqOrder = []
    for freqPair in freqPairs:
        freqOrder.append(freqPair[1])

    return ''.join(freqOrder)


def englishFreqMatchScore(message):
    '''Reutrns number of matches of the message
    with ETAOIN letters comparing with the first
    and the last six frequent letters'''
    freqOrder = getFrequencyOrder(message)

    matchScore = 0

    #finding matches of first six common letters
    for commonLetter in ETAOIN[:6]:
        if commonLetter in freqOrder[:6]:
            matchScore += 1

    #finding matches of least six common letters
    for commonLetter in ETAOIN[-6:]:
        if commonLetter in freqOrder[-6:]:
            matchScore += 1

    return matchScore







