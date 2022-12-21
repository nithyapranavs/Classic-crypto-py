#Babbage attack

import itertools, re
import vigenereCipher, freqAnalysis
from modules import detectEnglish

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SILENT_MODE = False  # if set to True, program doesn't print attempts
NUM_MOST_FREQ_LETTERS = 4  # attempts this many letters per subkey
MAX_KEY_LENGTH = 16  # will not attempt keys longer than this
NONLETTERS_PATTERN = re.compile('[^A-Z]')

def findRepeatSequencesSpacings(message):
    '''finds the repeated sequences and
    returns a dict with key as sequence and
    values of list of int spacing between the repeatents'''

    message = NONLETTERS_PATTERN.sub('',message.upper())

    seqSpacings = {}
    #key = sequences, value = list of in spacing

    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            seq = message[seqStart:seqStart+seqLen]

            #looking for the repeatences
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:#checking for repeatence
                    if seq not in seqSpacings:# checking for seq in dict already
                        seqSpacings[seq] = []

                    seqSpacings[seq].append(i - seqStart)
                    #appending the space distance between the repeated sequence

    return seqSpacings


def getUserfulFactors(num):
    '''Returns factor of num which is less than
    MAC_KEY_LENGTH + 1'''
    factors = []
    if num < 2:
        return factors

    for i in range(2,MAX_KEY_LENGTH +1):#not checking 1
        if num % i == 0:
            factors.append(i)
            factors.append(int(num/i))

    if 1 in factors:
        factors.remove(1)

    factors = list(set(factors))#removing duplicates

    return factors

def getItemAtIndexOne(x):
    return x[1]


def getMostCommonFactors(seqFactors):
    '''Returns most common factors in sorted list'''

    factorCounts = {}
    #key = factor, value = no. of occurs

    #seqFactors has a value like: {'GFD': [2, 3, 4, 6, 9, 12,
    # 18, 23, 36, 46, 69, 92, 138, 207], 'ALW': [2, 3, 4, 6, ...], ...}
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0

            factorCounts[factor] += 1

    factorsByCount = []
    #[(factor, factor count)...]
    for factor in factorCounts:
        if factor <= MAX_KEY_LENGTH:
            # (factor, factorCount)
            factorsByCount.append((factor, factorCounts[factor]))

    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)

    return factorsByCount


def kasiskiExamination(ct):
    '''Find out the sequences of 3 to 5 letters
     that occur multiple times'''

    repeatedSeqSpacings = findRepeatSequencesSpacings(ct)
    #values = {'EXG': [192], 'NAF': [339, 972, 633], ... }

    seqFactors = {}
    #key = seq, value = [factors]
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUserfulFactors(spacing))
            #extend function adds multiple item to the list

    factorsByCount = getMostCommonFactors(seqFactors)

    allLikelyKeyLengths = []
    #contains the most common factors
    for i in factorsByCount:
        allLikelyKeyLengths.append(i[0])

    return allLikelyKeyLengths


def getNthSubkeysLetters(n, keyLength, message):
    '''Returns every Nth letter for each
    keyLength set of letters in text.
     E.g. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns "AAA"'''

    message = NONLETTERS_PATTERN.sub('',message)

    i = n - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength

    return ''.join(letters)

def attemptHackWithKeyLength(ct, mostLikelyKeyLength):
    ctUp = ct.upper()

    # allFreqScores is a list of mostLikelyKeyLength number of lists.
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength +1):
        nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ctUp)

        freqScores = []
        # [(<letter>, <Eng. Freq. match score>), ... ]
        for possibleKey in LETTERS:
            decryptedText = vigenereCipher.decrypt(possibleKey, nthLetters)
            keyAndFreqMatch = (possibleKey, freqAnalysis.englishFreqMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatch)

        freqScores.sort(key=getItemAtIndexOne, reverse=True)

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    if not SILENT_MODE:
        for i in range(len(allFreqScores)):
            print('Possible letters for letter %s of the key: ' % (i + 1), end='')
            for freqScore in allFreqScores[i]:
                print('%s ' % freqScore[0], end='')
            print()

    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]
            # allFreqScores[i]-> freqScores
            # [indexes] -> accesses the tuple
            # [0] -> accesses the letter in the tuple

        if not SILENT_MODE:
            print('Attempting with key: %s' % (possibleKey))

        decryptedText = vigenereCipher.decrypt(possibleKey, ctUp)

        if detectEnglish.isEnglish(decryptedText):
            # Set the hacked ciphertext to the original casing.
            origCase = []
            for i in range(len(ct)):
                if ct[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())

            decryptedText = ''.join(origCase)


            # Check with user to see if the key has been found.
            print('Possible encryption hack with key %s:' % (possibleKey))
            print(decryptedText[:200]) # only show first 200 characters
            print()
            print('Enter D for done, or just press Enter to continue hacking:')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decryptedText

        #If No english-looking decryption found
        return None

def hackVigenere(ct):
    allLikelyKeyLengths = kasiskiExamination(ct)
    hackedMessage = None
    if not SILENT_MODE:
        keyLengthStr = ''
        for keyLength in allLikelyKeyLengths:
            keyLengthStr += '%s '% (keyLength)
        print('Kasiski Examination results say the most likely key lengths are: ' + keyLengthStr + '\n')

    for keyLength in allLikelyKeyLengths:
        if not SILENT_MODE:
            print('Attempting hack with key length %s (%s possible keys)...' % (
            keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        hackedMessage = attemptHackWithKeyLength(ct, keyLength)
        if hackedMessage != None:
            break

    if hackedMessage == None:
        if not SILENT_MODE:
            print('Unable to hack message with likely key length(s). Brute forcing key length...')

        for keyLength in range(1, MAX_KEY_LENGTH +1):
            if keyLength not in allLikelyKeyLengths:  #not re-checking already tried from kasiski
                if not SILENT_MODE:
                    print('Attempting hack with key length %s (%s possible keys)...' % (
                    keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                hackedMessage = attemptHackWithKeyLength(ct, keyLength)
                if hackedMessage != None:
                    break

    return hackedMessage

def main(ct):
    hackedMessage = hackVigenere(ct)

    if hackedMessage != None:
        print('Copying hacked message to clipboard:')
        print(hackedMessage)

    else:
        print("Failed to hack")

if __name__ == "__main__":
    ciphertext = """Adiz Avtzqeci Tmzubb wsa m Pmilqev halpqavtakuoi, lgouqdaf, kdmktsvmztsl, izr xoexghzr kkusitaaf. Vz wsa twbhdg ubalmmzhdad qz hce vmhsgohuqbo ox kaakulmd gxiwvos, krgdurdny i rcmmstugvtawz ca tzm ocicwxfg jf "stscmilpy" oid "uwydptsbuci" wabt hce Lcdwig eiovdnw. Bgfdny qe kddwtk qjnkqpsmev ba pz tzm roohwz at xoexghzr kkusicw izr vrlqrwxist uboedtuuznum. Pimifo Icmlv Emf DI, Lcdwig owdyzd xwd hce Ywhsmnemzh Xovm mby Cqxtsm Supacg (GUKE) oo Bdmfqclwg Bomk, Tzuhvif'a ocyetzqofifo ositjm. Rcm a lqys ce oie vzav wr Vpt 8, lpq gzclqab mekxabnittq tjr Ymdavn fihog cjgbhvnstkgds. Zm psqikmp o iuejqf jf lmoviiicqg aoj jdsvkavs Uzreiz qdpzmdg, dnutgrdny bts helpar jf lpq pjmtm, mb zlwkffjmwktoiiuix avczqzs ohsb ocplv nuby swbfwigk naf ohw Mzwbms umqcifm. Mtoej bts raj pq kjrcmp oo tzm Zooigvmz Khqauqvl Dincmalwdm, rhwzq vz cjmmhzd gvq ca tzm rwmsl lqgdgfa rcm a kbafzd-hzaumae kaakulmd, hce SKQ. Wi 1948 Tmzubb jgqzsy Msf Zsrmsv'e Qjmhcfwig Dincmalwdm vt Eizqcekbqf Pnadqfnilg, ivzrw pq onsaafsy if bts yenmxckmwvf ca tzm Yoiczmehzr uwydptwze oid tmoohe avfsmekbqr dn eifvzmsbuqvl tqazjgq. Pq kmolm m dvpwz ab ohw ktshiuix pvsaa at hojxtcbefmewn, afl bfzdakfsy okkuzgalqzu xhwuuqvl jmmqoigve gpcz ie hce Tmxcpsgd-Lvvbgbubnkq zqoxtawz, kciup isme xqdgo otaqfqev qz hce 1960k. Bgfdny'a tchokmjivlabk fzsmtfsy if i ofdmavmz krgaqqptawz wi 1952, wzmz vjmgaqlpad iohn wwzq goidt uzgeyix wi tzm Gbdtwl Wwigvwy. Vz aukqdoev bdsvtemzh rilp rshadm tcmmgvqg (xhwuuqvl uiehmalqab) vs sv mzoejvmhdvw ba dmikwz. Hpravs rdev qz 1954, xpsl whsm tow iszkk jqtjrw pug 42id tqdhcdsg, rfjm ugmbddw xawnofqzu. Vn avcizsl lqhzreqzsy tzif vds vmmhc wsa eidcalq; vds ewfvzr svp gjmw wfvzrk jqzdenmp vds vmmhc wsa mqxivmzhvl. Gv 10 Esktwunsm 2009, fgtxcrifo mb Dnlmdbzt uiydviyv, Nfdtaat Dmiem Ywiikbqf Bojlab Wrgez avdw iz cafakuog pmjxwx ahwxcby gv nscadn at ohw Jdwoikp scqejvysit xwd "hce sxboglavs kvy zm ion tjmmhzd." Sa at Haq 2012 i bfdvsbq azmtmd'g widt ion bwnafz tzm Tcpsw wr Zjrva ivdcz eaigd yzmbo Tmzubb a kbmhptgzk dvrvwz wa efiohzd."""
    main(ciphertext)












