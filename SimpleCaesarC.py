

#turn text into list of numbers (ASCII values)
import random


def encode(text):
    #turn to lower case
    text = text.lower()
    #only keep letters
    lst = [(ord(letter) - ord('a')) for letter in text if letter.isalpha()]
    return lst

#turn list of ASCII values into text
def decode(lst):
    text = ''.join([chr(ord('a')+code) for code in lst])
    return text

def shift(pt,k):
    'plaintext pt, shift k'
    ptlst = encode(pt)
    #shift each letter code by 26, and take result mod 26
    ctlst = [(x+k) % 26 for x in ptlst]
    return decode(ctlst)

#Function that uses a random number for shifting in the shift function
def cipherMe(pt):
    #random number for shifting
    randNum = random.random()*100
    randNum = int(randNum)
    #pt encoded, then shifted by randNum,
    #then decoded, stored in ptShift
    ptShift = shift(pt, randNum)
    return ptShift
    
#Function that attempts to break the Cipher Text using the heuristic...
#the letter "e" is the most common letter in the English alphabet
def simpleShiftBreak(ct):
    freqLst = {}
    #frequency analysis test
    for letter in ct:
        if( letter in freqLst):
            freqLst[letter] +=1
        else:
            freqLst[letter] =1
    #finding the most frequent letter
    mostFreq = max(freqLst, key = freqLst.get)
    encMF = encode(mostFreq)

    #Calculating the amount shifted for decryption purposes    
    shiftNum = encMF[0] - 4
    shiftNum = shiftNum%26
    dt = ""

    #Decrypting using shiftNum
    for letter in ct:
        x = encode(letter)
        shiftBack = (x[0]-shiftNum)%26
        x[0] = shiftBack
        x = decode(x)
        dt = dt+x
    return dt


def prepare(t):
    t = t.lower()
    s = ''
    for l in t:
        if l.isalpha():
            s += l
    return s

#gives an analysis on how well simpleShiftBreak decrypts
def testsimple(a,b):
    infile = open('innocents.txt', 'r')
    pt = infile.read()
    infile.close()
    pt = prepare(pt)
    
    tempPt = ''
    tempCt = ''
    count = 1
    statC = 0
    statW = 0
    statF = 0
    rangeCount = a
    while(rangeCount <= b):
        for t in pt:
            tempPt = tempPt + t
            if(count == rangeCount):
                tempCt = cipherMe(tempPt)
                tempCt = simpleShiftBreak(tempCt)
                if(tempCt == tempPt):
                    statC += 1
                    tempPt = ''
                    tempCt = ''
                    count = 1
                else:
                    statW += 1
                    tempPt = ''
                    tempCt = ''
                    count = 1
            else:
                count += 1
        if(statW != 0):
            statF = statC/float(statW+statC)
        else:
            statF = 1.0
        print "%d %.3f" % (rangeCount,statF)
        count = 1
        statC = 0
        statW = 0
        statF = 0
        tempPt = ''
        tempCt = ''
        rangeCount += 1

        
