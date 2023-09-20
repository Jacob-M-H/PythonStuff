

class FoundPotentialToken(): #The idea is that the sets_ will let us change the start/end when accpeting fair tokens across pairs and the unqiue list 
    symbolIndex:int #Which word in the sentence to look at for this token.
    tokenSymbol:str
    layer:int
    start:int
    end:int
    def __init__(self, tS:str, l:int, s:int, e:int, symbolIndex:int):
        self.symbolIndex=symbolIndex
        self.tokenSymbol=tS
        self.layer=l
        self.start=s
        self.end=e
    def getSymbolIndex(self):
        return self.symbolIndex
    def setSymbolIndex(self, idx:int):
        self.symbolIndex=idx
    def checkAssumptions(self):
        if self.layer>-1 and self.start>-1: #end is not clear, but start is.
            if self.start<=self.end:
                return 1
            else:
                return -1
        else:
            return -2
    def getTokenSymbol(self):
        return self.tokenSymbol
    def getLayer(self):
        return self.layer
    def setStart(self, s:int):
        self.start=s
    def setEnd(self, e:int):
        self.end=e
    def getStart(self):
        return self.start
    def getEnd(self):
        return self.end
    def __str__(self): #str(FoundPotentialToken) <-guess
        return "["+self.tokenSymbol+", "+ str(self.layer)+", "+str(self.start)+", "+str(self.end)+", "+str(self.symbolIndex)+"]"
    def __repr__(self): #print 
        return "["+self.tokenSymbol+", "+ str(self.layer)+", "+str(self.start)+", "+str(self.end)+", "+str(self.symbolIndex)+"]"
   





def markUp(inspectTokens, problemHighTokens):
    
    runningDifference=0
    insIdx=0
    while (len(inspectTokens)>insIdx):
        inspectToken=inspectTokens[insIdx]
        difference=inspectToken[1]-inspectToken[0]+1
        for token in problemHighTokens:
            if inspectToken[1]-runningDifference<token[0]: #ISSUES  
                print(inspectToken[1], "-", runningDifference,"<", token[0])
                token[0]=(token[0]-difference)
                token[1]=(token[1]-difference) 
        insIdx+=1
        runningDifference+=difference #DOES NOT MUTATE ORIGINAL acceptTokens LIST, AS WE NEED TO USE THE LIST AT LEAST TWICE
           

    return inspectTokens, problemHighTokens


#----- Find special Syntax and Conflicts in that (unintentional grammer conplexity) ----- 
#highTokens=findSpecialSyntax(wordList,"...", self.totalLayers) #Find potential recombinations of tokens for higher order tokens  
def fastFindSpecialSymbol1(wordList:list[str], specialSymbols:list[str], layer:int): #This function looks like it works best for 'highly recursive' string stuctures like ellipses, but otherwise too messy I think
    #Idea one:

    #Match Case
        #..., [0,0,0], 0  - sToken, arrayof Len(sToken), able to Iterate (max = len(sToken)-1)
    #for wordIdx in range(len(wordList)):
        #reset all cases to [0,0,0], 0 
        #word=wordList[wordIdx]
        #for chrIdx in range(len(wordList[wordIdx])): 
            #for sToken in sTokenList:
                #for i in range(0,stokenIterateAble+1):
                    #if word[chrIdx]==stoken[sTokenArray[i]]:
                        #stokenArray[i]+=1
                        #ableToIterate+=1
                        #if ableToIterate<len(stoken)-1:
                            #abletoIterate+=1
                        #if stokenArray[i]==len(sToken)-1:
                            #stokenArray[i]=0
                            #append(FoundPotentialToken)
                    #else:
                        #stokenArray[i]=0 #Broke chain -additional considerations are needed for cases like ..|...|....|... since failure messes up the abletoIterate idea.
    foundPotentialTokens=[]
    sTokenList=[]
    for symbol in specialSymbols:
        sTokenList.append([symbol, [0]*len(symbol), 0])
    for wordIdx in range(len(wordList)):
        if wordIdx!=0: #Reset sTokenInfo per word
            for sTokenInfo in sTokenList:
                for idx in range(len(sTokenInfo[0])):
                    sTokenInfo[1][idx]=0
                sTokenInfo[2]=0
        word =wordList[wordIdx]
        for chrIdx in range(len(word)):
            for sTokenInfo in sTokenList:
                symbolLength=len(sTokenInfo[0])  
                for i in range(sTokenInfo[2]+1): 
                    if word[chrIdx]==sTokenInfo[0][sTokenInfo[1][i]]:
                        sTokenInfo[1][i]+=1
                        if sTokenInfo[2]<symbolLength-1: #Note, this may be a problem, say in the case .....I.... we might end up all once again at the same, perhaps we can minus 1 when we fail? and shift right all the others? 
                            sTokenInfo[2]+=1 
                        if sTokenInfo[1][i]==symbolLength: #Found fill string
                            sTokenInfo[1][i]=0
                            foundPotentialTokens.append([(sTokenInfo[0], 0, chrIdx-symbolLength+1, chrIdx, wordIdx)]) #FoundPotentialToken basically
                    else:
                        sTokenInfo[1][i]=0
                        sTokenInfo[2]=0
    #I essentially temporarily double the specialtoken list. it's fine for small lists but on large langauges might become irksome.                        

    return foundPotentialTokens


    pass


def checkConflicts(highTokens:list[FoundPotentialToken]):
    highTokens.sort(key=lambda x:x.getSymbolIndex()) #We'll split the list by its index (since only if it's same word will it conflict) NOTE it is not necessarily the case that every word has a hightoken
    if len(highTokens)<=1:
        return [] #No possible problem pairs
    
    problemPairs=[]
    #ASSERT highTokesn must have at least two elements
    tempRun=[0,0]
    while tempRun[1]<len(highTokens):
        if highTokens[tempRun[0]].getSymbolIndex()==highTokens[tempRun[1]].getSymbolIndex():
            tempRun[1]+=1
        else:
            #print("Found run of ", tempRun[0], ", ",tempRun[1]-1)
            highTokens[tempRun[0]:tempRun[1]].sort(key=lambda x:(x.getEnd()-x.getStart()), reverse=True) #Widest range to start, mutates original list. 
            problemPairs.extend(checkConflictsHighTokens(highTokens[tempRun[0]:tempRun[1]])) 
            tempRun[0]=tempRun[1]
            tempRun[1]=tempRun[0]
    
    #print("Found run of ", tempRun[0], ", ",tempRun[1]-1)
    highTokens[tempRun[0]:tempRun[1]-1].sort(key=lambda x:(x.getEnd()-x.getStart()), reverse=True) #maybe this is redundant
    problemPairs.extend(checkConflictsHighTokens(highTokens[tempRun[0]:tempRun[1]]))
    return problemPairs

def checkConflictsHighTokens(highTokens:list[FoundPotentialToken]): #Could be improved. Runs only once per layer, after potential hightoken(s) are found.
    #Check just if there exists a conflict, report all idx's where the conflict occurs.
    #print("CCHT: ",highTokens) 
    highTokens.sort(key=lambda x:(x.getStart()), reverse=True) #In the event the tokens were not inserted correctly <- not necessary in practice, but perhaps might be in the future
    highTokens.sort(key=lambda x:(x.getEnd()-x.getStart()), reverse=True) #Widest range to start, mutates original list.  
    #print("CCHT sorted: ",highTokens)
    seenSpans=[]
    problemIdxPairs=[]
    problemFlag=False
    for token in highTokens: 
        for spanIdx in range(len(seenSpans)):
            span=seenSpans[spanIdx]
            #t.end=>s.start #t.start <= s.end #Both - russian doll (or neither?, the opposite, span is inside this span. Shouldn't happen since lambda sorts by span gap, )
            if token.getEnd()>=span.getStart() and token.getStart()<=span.getEnd(): #either one will be true 
                problemFlag=True
            elif span.getEnd()>=token.getStart() and span.getStart()<=token.getEnd():
                problemFlag=True
            else: #redundant but assured.
                problemFlag=False
            if problemFlag:
                problemIdxPairs.append([token, span])
                problemFlag=False
        seenSpans.append(token)  
    #Token in highTokens = [specialToken, Layer, st, end], conflict if they overlap between two or more tokens. [how to check multiple, unordered pairs?] [Order by widest span?]
   
    return problemIdxPairs #If not empty, the pairs are the problems.     
        


def sortBy(tokens:list[FoundPotentialToken], lambdaKeys:list):
    toDo=lambdaKeys[0]
    tokens.sort(key=toDo[0], reverse=toDo[1])
    #if there are more instructions, find runs and run those instructions on that subset
    if len(lambdaKeys)-1!=0:
        tempRun=[0,0]
        while tempRun[1]<len(tokens):
            if toDo[0](tokens[tempRun[0]])==toDo[0](tokens[tempRun[1]]):
                tempRun[1]+=1
            else:
                print("Found run of ", tempRun[0], ", ",tempRun[1]-1)
                tokens[tempRun[0]:tempRun[1]]=sortBy(tokens[tempRun[0]:tempRun[1]], lambdaKeys[1:]) #Widest range to start, mutates original list. 
                    #NOTE, I think the slicing when passing into sortBy makes it not sort in place :/. What can you do? I suppose. 
                tempRun[0]=tempRun[1]
                tempRun[1]=tempRun[0]
        
        print("Found run of ", tempRun[0], ", ",tempRun[1]-1)
        tokens[tempRun[0]:tempRun[1]]=sortBy(tokens[tempRun[0]:tempRun[1]], lambdaKeys[1:]) #Widest range to start, mutates original list.  

    return tokens





 
def breakUp(cpyWord:str, culprits:list[FoundPotentialToken]):
    adj=[]
    line=[]
    running=0
    adjIndex=0
    if culprits==[]:
        return [], []
    else:
        #print("Len of culrpits : ", culprits)
        adjIndex=0
        crime=culprits.pop(0) 
        f1=cpyWord[:crime.getStart()]
        f2=cpyWord[crime.getStart():crime.getEnd()+1]
        f3=cpyWord[crime.getEnd()+1:]
        running=crime.getEnd()+1
        adjIndex=1 #f2 !=""
        if f1!="":
            adjIndex+=1 
        #print("Found ", f1,", ",f2,", ", f3,", running: ", running)
        adj.append([crime.getSymbolIndex(), crime.getStart(), crime.getEnd(), adjIndex])
        line.append(f1)
        line.append(f2)

        while (len(culprits)>0):
            adjIndex=0
            cpyWord=f3
            #print("deal with remaining word(s): ", f3)
            if (cpyWord==""):
                break
            
            crime=culprits.pop(0)
            f1=cpyWord[:crime.getStart()-running]
            f2=cpyWord[crime.getStart()-running:crime.getEnd()+1-running]
            f3=cpyWord[crime.getEnd()+1-running:]
            running=crime.getEnd()+1
            adjIndex=1 #f2 !="" 
            #f2 !=""
            if f1!="":
                adjIndex+=1
            #print("Found ", f1,", ",f2,", ", f3,", running: ", running)
            adj.append([crime.getSymbolIndex(), crime.getStart(), crime.getEnd(), adjIndex])
            line.append(f1)
            line.append(f2)
    
        if f3!="":
            #print("final cpy word add (assuming it's either f3 or the last bit of last cpyWord): ", f3)
            line.append(f3) 
            adj.append([crime.getSymbolIndex(), crime.getEnd()+1, crime.getEnd()+len(cpyWord), 1]) #Only one additional left
        return line, adj


def acceptToken(wordList:list[str], inspectTokens:list[FoundPotentialToken]):
    inspectIdx=0
    if len(inspectTokens)==0:
        return wordList, []
    print(wordList, inspectTokens)
    inspectToken=inspectTokens[inspectIdx]
    newLine=[]
    culprits=[]
    adjustSurvivors=[]#insert error if there is a Token with a wordIndex beyond our wordList (early sanity check)
    for wordIdx in range(len(wordList)): 
        print("1")
        cpyWord=wordList[wordIdx]
        if wordIdx<inspectToken.getSymbolIndex() or len(inspectTokens)==inspectIdx:
            print("2")
            newLine.append(cpyWord)
        else: 
            print("3")
            while wordIdx==inspectToken.getSymbolIndex():
                print("3.5")
                if len(inspectTokens)==inspectIdx: 
                    break
                else:
                    print("5")
                    culprits.append(inspectToken)
                    inspectIdx+=1
                    if inspectIdx<=len(inspectTokens)-1:
                        print("6")
                        inspectToken=inspectTokens[inspectIdx]
                
                
            x,y=breakUp(cpyWord, culprits) #returns a list to join with the new line, and a list to join with the adjust 
            culprits=[]
            newLine.extend(x)
            adjustSurvivors.extend(y)
            print("7")

    print("hm ", newLine)
    return newLine, adjustSurvivors
 

def problemPairSanityCheck(survivorProblemList, problemPairs):
    pass

def adjustTokens(survivorFairList:list[FoundPotentialToken], adjustList:list[list[int, int, int, int]]):
    
    def addRunning(running, Adj):
        if running[0]==nextAdj[0]:
            running[1]=nextAdj[1]
            running[2]=nextAdj[2]
            running[3]+=nextAdj[3]
        else:
            running[0]=nextAdj[0]
            running[1]=0
            running[2]=0
            running[3]=0
        return running
    def addChange(running, fairTkn:FoundPotentialToken):
        newStart=fairTkn.getStart()-running[2] #old start - running end
        newEnd=newStart+ fairTkn.getEnd()-fairTkn.getStart()+1
        newSymbolIdx=running[3] + fairTkn.getSymbolIndex()
        fairTkn.setStart(newStart)
        fairTkn.setEnd(newEnd)
        fairTkn.setSymbolIndex(newSymbolIdx) 

    #adjust list : [word index [original], start, end, indexAdjust]
    running=[0,0,0,0]
    #assuming survivor fair list and problem lists are sorted by wordIndx, then by start
    adjustIdx=0
    fairIdx=0
    runningDiff=0 #might need but hard to grasp.
    if len(survivorFairList)==0:
        return
    if len(adjustList)==0:
        return

    while adjustIdx<len(adjustList) and fairIdx<len(survivorFairList):
        print("1")
        fairTkn=survivorFairList[fairIdx]
        nextAdj=adjustList[adjustIdx]
        if nextAdj[0]==fairTkn.getSymbolIndex():
            if nextAdj[2]>fairTkn.getStart():
                print("2")
                addChange(running, fairTkn)
                fairIdx+=1 
            else:
                print("3")
                running=addRunning(running, nextAdj)
                adjustIdx+=1
        else:
            if nextAdj[0]>fairTkn.getSymbolIndex(): 
                print("4")
                fairIdx+=1 #Catch up to when we can actually use running basically
            else: #nextAdj<fairTkn getsymbol
                print("5")
                running=addRunning(running, nextAdj) #Need the total idx adjustments.

    while fairIdx<len(survivorFairList) and adjustIdx==len(adjustList): #try to catch case when there is no nextAdjust, and wrap up all the remaining     
        if running[0]==fairTkn.getSymbolIndex():
            if running[2]<fairTkn.getStart():
                print("6")
                addChange(running, fairTkn)
                fairIdx+=1 
            else:
                print("7")
                break
        else:
            if running[0]>fairTkn.getSymbolIndex(): 
                print("8")
                fairIdx+=1 #Catch up to when we can actually use running basically
            else: #nextAdj<fairTkn getsymbol
                print("9")
                break #No more adjusts we can make


    pass


def main():
    test=""    
    if (test=="markUp"):
        fairTokens=[ [1,3],[5,7],[15,17],[24,26] ]
        
        problemTokens=[ [11,13], [10, 12], [ 9, 11], [20, 22], [19, 21]]
        #expect PB =  [ [ 5, 7], [ 4,  6], [ 3,  5], [11, 13], [10, 12] ]
        fairTokens, problemTokens=markUp(fairTokens, problemTokens)
        print(problemTokens)
        
        problemTokens=[ [11,13], [10, 12], [ 9, 11], [19, 21], [20, 22]]
        #expect PB =  [ [ 5, 7], [ 4,  6], [ 3,  5], [10, 12], [11, 13] ]
        fairTokens, problemTokens=markUp(fairTokens, problemTokens)
        print(problemTokens)

        problemTokens=[ [19, 21] ]
        #expect PB =  [ [10, 12] ]
        fairTokens, problemTokens=markUp(fairTokens, problemTokens)
        print(problemTokens)

    if test=="fastFindSpecialSymbol1":

        def run(wordList, specialSymbols):
            highTokens=fastFindSpecialSymbol1(wordList, specialSymbols, 0)
            print(highTokens)#token, layer, start, end, wordIdx
        specialSymbols=["..."] #Test with one specail symbol for starters
        #Exhause basic finds
        wordList=["..."]
        run(wordList, specialSymbols) #expect ['...', 0, 0, 2, 0] 
        wordList=["...."]#expect ['...', 0, 0, 2, 0] , ['...', 0, 1, 3, 0] 
        run(wordList, specialSymbols)
        wordList=["....."]#expect ['...', 0, 0, 2, 0] , ['...', 0, 1, 3, 0] , ['...', 0, 2, 4, 0]
        run(wordList, specialSymbols)
        wordList=["......"]#expect ['...', 0, 0, 2, 0] , ['...', 0, 1, 3, 0] , ['...', 0, 2, 4, 0] , ['...', 0, 3, 5, 0]
        run(wordList, specialSymbols)
        print("completed basic finds")
        wordList=["...|"]#expect ['...', 0, 0, 2, 0] 
        run(wordList, specialSymbols)
        wordList=["...|."]#expect ['...', 0, 0, 2, 0]  
        run(wordList, specialSymbols)
        wordList=["...|.."]#expect ['...', 0, 0, 2, 0]  
        run(wordList, specialSymbols)
        wordList=["...|..."]#expect ['...', 0, 0, 2, 0] , ['...', 0, 4, 6, 0] 
        run(wordList, specialSymbols)
        wordList=["....|"]#expect ['...', 0, 0, 2, 0] , ['...', 0, 1, 3, 0] 
        run(wordList, specialSymbols) 
        wordList=[".....|."]#expect ['...', 0, 0, 2, 0] , ['...', 0, 1, 3, 0] , ['...', 0, 2, 4, 0] 
        run(wordList, specialSymbols) 
        wordList=["......|.."]#expect ['...', 0, 0, 2, 0] , ['...', 0, 1, 3, 0] , ['...', 0, 2, 4, 0] , ['...', 0, 3, 6, 0] 
        run(wordList, specialSymbols) 
        print("Completed pre stops")
        wordList=["......|...."] #expect ['...', 0, 0, 2, 0] , ['...', 0, 1, 3, 0] , ['...', 0, 2, 4, 0] , ['...', 0, 3, 6, 0] , ['...', 0, 7, 9, 0] , ['...', 0, 8, 10, 0] 
        run(wordList, specialSymbols) 
        wordList=["...||...|."] #expect ['...', 0, 0, 2, 0] , ['...', 0, 5, 7, 0] 
        run(wordList, specialSymbols) 
        wordList=["...||...|....|||....||...."] #expect ['...', 0, 0, 2, 0] , ['...', 0, 5, 7, 0] , ['...', 0, 9, 11, 0] , ['...', 0, 10, 12, 0] , ['...', 0, 16, 18, 0] , ['...', 0, 17, 19, 0] , ['...', 0, 22, 24, 0] , ['...', 0, 23, 25, 0] 
        run(wordList, specialSymbols) 
        print("Completed stop and begins")
        specialSymbols=["...",",,,","....","...,","..,.",".||."] #More variety, see if tracking works well with the ..,., and the .||. or if the array fails. If the array fails, may have to reset the array on failure and that might fix? Be sure not to break the above cases!
        wordList=["..,.||....,,,"] #expect 7 tokens
        run(wordList, specialSymbols) 

        print("completed variety high tokens")



        pass
 
    if test=="checkConflicts":
        pairs=checkConflicts([])
        #[symbol, layer, start, end, wordIdx]
        print("result :", pairs)
        pairs=checkConflicts([FoundPotentialToken("...", 0,  0, 2, 0)])
        print("result :", pairs)

        print("2 tokens")
        pairs=checkConflicts([FoundPotentialToken("...", 0,  0, 2, 0),
                              FoundPotentialToken("...", 0,  0, 2, 1)]) #different word, same span, same symbol
        
        print("result :", pairs)
        pairs=checkConflicts([FoundPotentialToken("...", 0,  0, 2, 0),
                              FoundPotentialToken("...", 0,  1, 3, 0)]) #same word, same span, same symbol
        
        print("result :", pairs)
        pairs=checkConflicts([FoundPotentialToken("...", 0,  1, 3, 0),
                              FoundPotentialToken("...", 0,  0, 2, 0)])  #same word, wrong order  (This doesn't happen in my code, but to be safe should sort by start once more...?)
        print("result :", pairs)
        pairs=checkConflicts([FoundPotentialToken("...", 0,  0, 2, 0),
                              FoundPotentialToken("...", 0,  1, 3, 0), 
                              FoundPotentialToken("...", 0,  2, 4, 0),
                              FoundPotentialToken("...", 0,  0, 2, 1),
                              FoundPotentialToken("...", 0,  3, 5, 1), 
                              FoundPotentialToken("...", 0,  3, 5, 2)])  #same word, wrong order  (This doesn't happen in my code, but to be safe should sort by start once more...?)
        print("result :", pairs)
 
    if test=="sortBy":
        outOfOrder=[ 
                                FoundPotentialToken("...", 0,  1, 3, 0), 
                                FoundPotentialToken("...", 0,  3, 5, 2),
                                FoundPotentialToken("...", 0,  0, 2, 0), 
                                FoundPotentialToken("...", 0,  2, 4, 0),
                                FoundPotentialToken("...", 0,  3, 5, 1),
                                FoundPotentialToken("...", 0,  0, 2, 1) 
                                ]
        sortBy(outOfOrder, [[lambda x:x.getSymbolIndex(), False], [lambda x:x.getStart(), False]])
        print(outOfOrder)
    
    test="createNewLine2"
    if test=="createNewLine2":
        inOrderSurvivor=[FoundPotentialToken("...", 0, 5, 7, 0)] 
        wordList=["Jacob...,,...",]
        line, adjusts=acceptToken(wordList, inOrderSurvivor)
        print("resulting line: ",line)
        print("adjustments : ", adjusts)
        print("BREAK")

        inOrder=[FoundPotentialToken("...", 0, 5, 7, 0),
                 FoundPotentialToken("...", 0, 10, 12, 0)]
        wordList=["Jacob...,,...",]
        line, adjusts=acceptToken(wordList, inOrder)
        print("resulting line: ",line)
        print("adjustments : ", adjusts)
        print("BREAK")
        
        inOrder=[FoundPotentialToken("...", 0, 5, 7, 0),
                 FoundPotentialToken("...", 0, 10, 12, 0)]
        wordList=["Jacob...,,...,",]
        line, adjusts=acceptToken(wordList, inOrder)
        print("resulting line: ",line)
        print("adjustments : ", adjusts)
        print("BREAK")

    test=" "
    if test=="adjustTokens":
    #survivorFairList:list[FoundPotentialToken], adjustList:list[list[int, int, int, int]]
        #TESTS BASED ON CREATENEWLINE returns
        inOrderSurvivor=[FoundPotentialToken("...", 0, 5, 7, 0)] 
        wordList=["Jacob...,,...",]
        line, adjusts=acceptToken(wordList, inOrderSurvivor)
        print("resulting line: ",line)
            #adjust=[[0,5,7,2]] LATER AFTER THE ACCEPT IS FIXED
            #adjustTokens(inOrderSurvivor, adjust)
            #print(inOrderSurvivor)

    #When adjusting, if we had more than 1 split... I wonder about it... I think it's fine... [symbol index, start end of word, and indexes t oadjust by [add to it]]
    



if __name__=="__main__":
    main()