"""
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



mystring = "taxus"
mystring2 = "stott"
print(check_peg(mystring, mystring2))
print(int(ternaryToDec(check_peg(mystring, mystring2))))
"""
"""
a = ["a", "b", "c", "d", "e"]
print(a)
print(a[:])
for item in a:
    print(item)
a[:] = []
print(a)
print(a[:])
a= []
print(a)
print(a[:])
"""

def ternaryToKey(peg):
    myString = str()
    for i in range(5):
        q, mod = divmod(peg, 10**(4-i))
        print(q,mod)
        peg = mod
        if (q == 2):
            myString= myString + "c"
        elif (q == 1):
            myString= myString + "p"
        else:
            myString= myString + "n"
    return myString

print(ternaryToKey(12100))