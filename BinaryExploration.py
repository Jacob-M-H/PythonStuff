#originates from sig fig project, which is a part of a JS chemistry project.
    #Desire to have binary operations that may fix the odd number issue in JS.

from SigFigs import SigFig 
from sys import byteorder
from math import ceil 

#NOTE for when returning, the subtraction algorithm is a bit wonky, but pen/paper seemed to work, so somethings off. Wrote it in my chem notes.

def addPadding(value:str, amt):
    return value[0:2]+("0"*amt)+value[2:]

PADDING=32 #pad bytes to 32
def printNumberAsBinary(value)->str:
    leftBits=bin(value) 
    if leftBits[0]=="-": #2's' compilment
        leftBits="1"+leftBits[2:] #str are immutable, so have to do this. 
    pad=0
    if len(leftBits)-2>PADDING:
        raise ValueError("warning, exceeded padding")
    else:
        pad="0"*(PADDING-len(leftBits)+1)  
    return leftBits[0] + "b"+ pad + leftBits[2:] #preserve the sign, byte, padding, and inital bits

def printBinaryAsNumber(value)->int:
    if value[0]=="1": #2's compilment
        value="-0"+value[1:]
    return int(value, 2)
 

def XOR(bin1:str, bin2:str):
    if len(bin1)!=len(bin2): 
        if len(bin1)<len(bin2):
            bin1=addPadding(bin1, len(bin2)-len(bin1))
        else:
            bin2=addPadding(bin2, len(bin1)-len(bin2))
    
    newBin=""
    #sign
    if bin1[0]!=bin2[0]:
        newBin+="1b"
    else:
        newBin+="0b"
    
    goal=len(bin1)
    i=2
    dropNeg=True
    while i<goal:
        true=bin1[i]!=bin2[i]
        if true:
            newBin+="1"
            dropNeg=False
        else:
            newBin+="0"
        i+=1
    if dropNeg==True:
        newBin="0"+newBin[1:]
    return newBin

def printNumberBinaryPair(value)->str: 
    if type(value)==str: 
        return str(printBinaryAsNumber(value))+": "+value
    else:
        return str(value)+": "+printNumberAsBinary(value)

def NOT(bin:str):
    newBin=""
    for i in range(len(bin)):
        if bin[i]=="0":
            newBin+="1"
        elif bin[i]=="1":
            newBin+="0"
        else:
            newBin+="b"
    return newBin

def AND(bin1:str, bin2:str): #insert check padding
    newBin=""
    if bin1[0]==bin2[0]:
        newBin+="1"
    newBin+="b"

    for i in range(2,len(bin1)):
        if bin1[i]==bin2[i]:
            newBin+="1"
        else:
            newBin+="0"
    return newBin



#https://www.geeksforgeeks.org/reverse-string-python-5-different-ways/
def reverse(s):
    if len(s) == 0:
        return s
    else:
        return reverse(s[1:]) + s[0]


#taking quick break, my logic is sound but clealry I messed up programming somehwere.
def SUB(bin1:str, bin2:str): #INSERT check if negative sub/sub negative [in that case return ADD[bin1, pos bin2]]
    carryBit="0"
    newBin=""
    #INSERT padding check
    bin1=bin1[2:] 
    bin2=bin2[2:]
    #it'd be best to reverse bin1, bin2 first, but who knows.
    i=len(bin1)-1
    while (i>-1):
        print(bin1[i], bin2[i], carryBit, end=" ")
        if bin1[i]=="0" and bin2[i]=="1":
                #Note if we already have a carry bit, the carry bit automtically 'carries' itself.
                carryBit="1"
                newBin+="1"  #carry bit required, and place a 1 in this spot assuming we catch up
        elif bin1[i]=="1" and bin2[i]=="0":
                #CHeck carry bit, otherwise place a 1 bit, reset carry bit
                if carryBit=="1":
                    carryBit="0"
                    newBin="0"
                else:
                    newBin+="1"
        else:
            newBin+="0" #carry bit still carried.
        print(newBin[len(newBin)-1])
        i-=1
    #again, 0b is presumptious      
    return "0b"+reverse(newBin)


def main(): 
    print(printBinaryAsNumber(printNumberAsBinary(63)))
    print(printBinaryAsNumber(printNumberAsBinary(31)))
    print(printBinaryAsNumber(printNumberAsBinary(-31)))
    v1=printNumberAsBinary(63)
    v2=printNumberAsBinary(31)
    v3=printNumberAsBinary(-31)
  
    print(printNumberBinaryPair(XOR(v1,v2)))
    print(printNumberBinaryPair(XOR(v2,v3)))
    print(printNumberBinaryPair(XOR(v1,v3)))
    #Subtraction, XOR(smaller value)+largerValue, omit the carry [always carry in this case?]
    #one's complment = !(binary value)
        #2's complement = !(binary value)+'1' (at very left side), so 5->0101, !(0101)+1 = 1011
    print(v1)
    print(NOT(v1)) 
    print(AND(v1,v2))  

    v4=printNumberAsBinary(78)
    v5=printNumberAsBinary(31)
    print(printNumberBinaryPair(v4))
    print(printNumberBinaryPair(v5))
    print(printNumberBinaryPair(SUB(v4, v5)))

    pass


if __name__=="__main__":
    main()