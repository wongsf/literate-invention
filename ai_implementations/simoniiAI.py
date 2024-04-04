import string
import numpy as np
import sys

from WordleAI import WordleAI, LetterInformation

class simoniiAI(WordleAI):
    def guess(self, guess_history):
        guess_number = len(guess_history)
        #print("Guess Number:", guess_number)
        #for i in range(guess_number):
        #    print(guess_history[i])
        
        if  guess_number < 1:
            next_guess = "serai"
        elif guess_number < 2:
            d1={}
            with open("simoniiCache1.txt") as f1:
                for line in f1:
                    (key, val) = line.split()
                    d1[str(key)]=str(val)
            #print(guess_history[0][1])
            #print(guess_hist2key(guess_history[0][1]))
            #print(d1[guess_hist2key(guess_history[0][1])])
            next_guess = d1[guess_hist2key(guess_history[0][1])]
            #print("it's in d1", guess_hist2key(guess_history[0][1]))
        elif guess_number < 3:
            d2={}
            with open("simoniiCache2.txt") as f2:
                for line in f2:
                    (key, val) = line.split()
                    d2[str(key)]=str(val)
            #print(guess_history[0][1])
            #print(guess_hist2key(guess_history[0][1]))
            #print(d1[guess_hist2key(guess_history[0][1])])
            next_guess = d2[guess_hist2key(guess_history[0][1])+guess_hist2key(guess_history[1][1])]
            #print("it's in d2",guess_hist2key(guess_history[0][1])+guess_hist2key(guess_history[1][1]))    
        else:
            options = remaining_options(self.words, guess_history)  # take known information into account
            #print("Options left:", len(options))
            #for option in options:
            #    print(option)
            if len(options)>1:
                pegCounts = 0
                pcIdx= 0
                tempMinCounts = sys.maxsize
                next_guess = self.words[0] ######## Replace by options if hard mode
                for word in self.words: ######## Replace by options if hard mode
                    pegList = [0] * 243
                    for option in options:
                        tempPegDec = int(ternaryToDec(check_peg(word , option)) )
                        #if tempPegDec>242:
                        #print(word, option, tempPegDec)
                        pegList[tempPegDec] +=  1
                    pegCounts= max(pegList)
                    if pegCounts < tempMinCounts:
                        next_guess = word
                        tempMinCounts = pegCounts
                    elif pegCounts == tempMinCounts and (word in options):
                        next_guess = word
            elif len(options) == 1:
                next_guess = options[0]
            else:
                next_guess = "XXXXX"
        #print(next_guess)
        return next_guess
    
    def get_author(self):
        return "simonii"
    
#my_array = [0 for a in range(3)]  or my_array = [0]*3 --->  my_array = [0,0,0]

def guess_hist2key(guess_result): # from guess_result to nnnnn format
    myString = str()
    for i in range(5):
            if guess_result[i] == LetterInformation.CORRECT:
                myString = myString + str("c")
            elif guess_result[i]== LetterInformation.PRESENT:
                myString = myString + str("p")
            else:
                myString = myString + str("n")
    return myString

def ternaryToKey(peg):
    myString = str()
    for i in range(5):
        q, mod = divmod(peg, 10**(4-i))
        peg = mod
        if (q == 2):
            myString= myString + "c"
        elif (q == 1):
            myString= myString + "p"
        else:
            myString= myString + "n"
    return myString
            

def check_peg(strInput, ansInput):
    flagi= [bool(1),bool(1),bool(1),bool(1),bool(1)]  #'true = need to be checked'
    flagj= [bool(1),bool(1),bool(1),bool(1),bool(1)]  #'true = need to be checked'
    peg=0
    for i in range(5):
        if(strInput[i]==ansInput[i]):
            peg += 2 *(100000/(10**(i+1)))
            flagi[i]=bool(0)
            flagj[i]=bool(0)
    for i in range(5):
        for j in range(5):
            if flagi[i]:
                if flagj[j]:
                    if strInput[i]==ansInput[j]:
                        peg += 100000/(10**(i+1))
                        flagi[i]=bool(0)
                        flagj[j]=bool(0)
                        j=6
    return peg

def ternaryToDec(peg):
    temp = 0
    digit = 0
    while peg > 0:
        q, mod = divmod(peg,10)
        peg = q
        temp = temp + mod * (3**digit)
        digit = digit + 1
    return temp


                    
    
def remaining_options(words, guess_history):
    """
    Filters a word list with all the known information.
    Returns the list of remaining options.
    
    present = set()
    not_present = set()
    correct = set()
    present_letters = set()
    for entry in guess_history:
        for i in range(5):
            if entry[1][i] == LetterInformation.CORRECT:
                correct.add((entry[0][i], i))
                present_letters.add(entry[0][i])
            elif entry[1][i] == LetterInformation.PRESENT:
                present.add((entry[0][i], i))
                present_letters.add(entry[0][i])
            else:
                not_present.add(entry[0][i])

    for c in present_letters:
        words = [w for w in words if c in w]
    for c in not_present:
        words = [w for w in words if c not in w]
    for c in correct:
        words = [w for w in words if w[c[1]] == c[0]]
    for c in present:
        words = [w for w in words if w[c[1]] != c[0]]
    """
    tempWords1 = words
    guess_number = len(guess_history)
    for i in range(guess_number):
        tempWords2 = []
        guess1 = guess_history[i][0]
        guess_result= guess_history[i][1]
        for word in tempWords1:
            if ternaryToKey(check_peg(guess1, word))==guess_hist2key(guess_result):
                #print(guess_hist2key(guess_result), word)
                tempWords2.append(word)
        print("Options left: ", len(tempWords2))
        tempWords1 = tempWords2
    
    return tempWords2