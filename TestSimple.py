

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
        crime=culprits.pop(0) 
        RunStart=0
        ADJIDX=1
        SYMIDX=crime.getSymbolIndex() 

        f1=cpyWord[:crime.getStart()]
        f2=cpyWord[crime.getStart():crime.getEnd()+1]
        f3=cpyWord[crime.getEnd()+1:]
        running=crime.getEnd()+1 
        if f1!="":
            adj.append([SYMIDX, RunStart, crime.getStart()-1, ADJIDX]) 
            line.append(f1) 
        adj.append([SYMIDX, crime.getStart(), crime.getEnd(), ADJIDX]) 
        line.append(f2)
        RunStart=crime.getEnd()+1 

        while (len(culprits)>0):  
            cpyWord=f3
            #print("deal with remaining word(s): ", f3)
            if (cpyWord==""):
                break
            
            crime=culprits.pop(0)
            f1=cpyWord[:crime.getStart()-running]
            f2=cpyWord[crime.getStart()-running:crime.getEnd()+1-running]
            f3=cpyWord[crime.getEnd()+1-running:]
            running=crime.getEnd()+1  
            if f1!="":
                adj.append([SYMIDX, RunStart, crime.getStart()-1, ADJIDX]) 
                line.append(f1) 
            adj.append([SYMIDX, crime.getStart(), crime.getEnd(), ADJIDX]) 
            line.append(f2)
            RunStart=crime.getEnd()+1
    
        if f3!="":# in the event len(culprits)==0) 
            start=max(crime.getEnd()+1, RunStart) 
            adj.append([SYMIDX, start, start+len(f3)-1, ADJIDX]) #Only one additional left
            line.append(f3) 

        return line, adj


def acceptToken(wordList:list[str], inspectTokens:list[FoundPotentialToken]):
    inspectIdx=0
    if len(inspectTokens)==0:
        return wordList, [] 
    inspectToken=inspectTokens[inspectIdx]
    newLine=[]
    culprits=[]
    adjustSurvivors=[]#insert error if there is a Token with a wordIndex beyond our wordList (early sanity check)
    for wordIdx in range(len(wordList)):  
        cpyWord=wordList[wordIdx]
        if wordIdx<inspectToken.getSymbolIndex() or len(inspectTokens)==inspectIdx: #Might be an unncessary econd condition here [eh, fine I think in event inspectIdx over extends]
            #print("Needs testing!") #NOTE TEST ME, jacob...,,... x2, and only take both high tokens fro the first. triggers.
            newLine.append(cpyWord)
        else:  
            while wordIdx==inspectToken.getSymbolIndex(): 
                if len(inspectTokens)==inspectIdx: 
                    break
                else: 
                    culprits.append(inspectToken)
                    inspectIdx+=1
                    if inspectIdx<=len(inspectTokens)-1: 
                        inspectToken=inspectTokens[inspectIdx]
                
                
            x,y=breakUp(cpyWord, culprits) #returns a list to join with the new line, and a list to join with the adjust 
            culprits=[]
            newLine.extend(x)
            adjustSurvivors.extend(y) 
 
    return newLine, adjustSurvivors
 

def problemPairSanityCheck(survivorProblemList, problemPairs):
    pass

def adjustTokens(survivorFairList:list[FoundPotentialToken], adjustList:list[list[int, int, int, int]]):
    
    def addRunning(running, Adj): 
        running[0]=nextAdj[0]
        running[1]=nextAdj[1]
        running[2]=nextAdj[2]
        running[3]+=nextAdj[3]
        return running
    
    def addChange(running, fairTkn:FoundPotentialToken):
        newStart=fairTkn.getStart()-running[2]-1 #old start - running end
        newEnd=newStart+ fairTkn.getEnd()-fairTkn.getStart()
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
    print(adjustList, "\n", survivorFairList,"\n")
    while adjustIdx<len(adjustList) and fairIdx<len(survivorFairList):
        print("1")
        fairTkn=survivorFairList[fairIdx]
        nextAdj=adjustList[adjustIdx]
        if nextAdj[0]==fairTkn.getSymbolIndex():
            if nextAdj[2]>fairTkn.getStart():
                print("2")
                if running[2]<fairTkn.getStart() and running[2]!=0: #NOTE, test a hightoken of length 1! 
                    print("2.5")
                    #If running[2]=0, and [1]=0, then we aren't to move it at all. But if they are the same maybe?
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
                while (nextAdj[0]<fairTkn.getSymbolIndex()):
                    running=addRunning(running, nextAdj) #Need the total idx adjustments.
                    adjustIdx+=1 
                    if adjustIdx<len(adjustList):
                        nextAdj=adjustList[adjustIdx]
                    else: 
                        break #Breaks out to if running[3]>0
                #Maybe adjustrunning once more to get teh symbols right?



    print("check up: ", running)
        #if running[3]>0:
        #    running[3]-=1  #??? When we skip ahead, then we should subtract one maybe from running?

    #If fairIdx=>len(survivor) and adjustIdx==len(adjustList):
        #Maybe subtract one from the adjustIdx? or running?
    while fairIdx<len(survivorFairList) and adjustIdx==len(adjustList): #try to catch case when there is no nextAdjust, and wrap up all the remaining   
        fairTkn=survivorFairList[fairIdx] #This might need to be at teh start/end of the loop... Who knows?  



        print("-1") 
        if running[0]<=fairTkn.getSymbolIndex():
            if running[2]<fairTkn.getStart() and running[0]==fairTkn.getSymbolIndex():
                print("6")
                addChange(running, fairTkn)
                fairIdx+=1 
            elif running[0]<fairTkn.getSymbolIndex():
                print("6.5") 
                fairTkn.setSymbolIndex(running[3] + fairTkn.getSymbolIndex() )
                fairIdx+=1 
                #TROUBLE, this was just a long shot. But didn't work. :/ may need to jostle aroudn
                if running[3]>0:
                    running[3]-=1   #??? When we skip ahead, then we should subtract one maybe from running?

            else:
                print("7")
                break
        else:
            if running[0]>fairTkn.getSymbolIndex(): 
                print("8")
                fairIdx+=1 #Catch up to when we can actually use running basically
            else: #running[0] <fairTkn getsymbol
                print("9") #Should be impossible
                break #No more adjusts we can make

         

        
    pass


def adjustTokens2(tokenList:list[FoundPotentialToken], adjustList:list[list[int,int,int,int]]):
    
    def addRunning(running, Adj): 
        running[0]=nextAdj[0]
        running[1]=nextAdj[1]
        running[2]=nextAdj[2]
        running[3]+=nextAdj[3]
        return running
    
    def addChange(running, tkn:FoundPotentialToken): #Might have issues at tkn lengths of 1
        if running != [0,0,0,0]:
            newStart=tkn.getStart()-running[2]-1 #old start - running end
        else:
            newStart=tkn.getStart()-running[2] #forcible solution :/
            
        newEnd=newStart+ tkn.getEnd()-tkn.getStart()
        newSymbolIdx=running[3] + tkn.getSymbolIndex() 
        tkn.setStart(newStart)
        tkn.setEnd(newEnd)
        tkn.setSymbolIndex(newSymbolIdx) 
 
    #assuming survivor fair list and problem lists are sorted by wordIndx, then by start
    running=[0,0,0,0]
    adjIdx=0
    tknIdx=0
    #Base case
    if len(tokenList)==0:
        return tokenList, adjustList
    if len(adjustList)==0:
        return tokenList, adjustList
    print(adjustList, "\n", tokenList)
    #INSERT _ if adjustList >=2 length, set running to be first [0], and adjIdx=1. And make a seperte case if the length is just of 1.
    while adjIdx<len(adjustList) and tknIdx<len(tokenList):
        print("1")
        tkn=tokenList[tknIdx]
        nextAdj=adjustList[adjIdx]
        if nextAdj[0]<tkn.getSymbolIndex():
            print("5")
            running=addRunning(running, nextAdj)
            adjIdx+=1
        else:
            if nextAdj[0]>tkn.getSymbolIndex():
                print("4")
                addChange(running, tkn)
                tknIdx+=1
            else: # nextAdj[0]==tkn.getSymbolIdx():
                if nextAdj[2]<tkn.getStart(): #Must allow running to be 0... I think? Otherwise need to make sure running is set to at least the first next, and then run this loop only if the list is longer than 2
                    print("3")
                    running=addRunning(running, nextAdj)
                    adjIdx+=1
                else:
                    print("2")
                    addChange(running, tkn)
                    tknIdx+=1
        


    print("check up: ", running)
    #Did not alter this beyond copy paste from adjust1.
    while tknIdx<len(tokenList) and adjIdx==len(adjustList): #try to catch case when there is no nextAdjust, and wrap up all the remaining   
        tkn=tokenList[tknIdx] #This might need to be at teh start/end of the loop... Who knows?   
        print("-1") 
        if running[0]<=tkn.getSymbolIndex():
            if running[2]<tkn.getStart() and running[0]==tkn.getSymbolIndex():
                print("6")
                addChange(running, tkn)
                tknIdx+=1 
            elif running[0]<tkn.getSymbolIndex():
                print("6.5") 
                tkn.setSymbolIndex(running[3] + tkn.getSymbolIndex() )
                tknIdx+=1 
                #TROUBLE, this was just a long shot. But didn't work. :/ may need to jostle aroudn
                if running[3]>0:
                    running[3]-=1   #??? When we skip ahead, then we should subtract one maybe from running? 
            else:
                print("7")
                break
        else:
            if running[0]>tkn.getSymbolIndex(): 
                print("8")
                tknIdx+=1 #Catch up to when we can actually use running basically
            else: #running[0] <fairTkn getsymbol
                print("9") #Should be impossible
                break #No more adjusts we can make

    pass



def adjustTokens3(tokenList:list[FoundPotentialToken], adjustList:list[list[int,int,int,int]]): 
    #Base case
    if len(tokenList)==0:
        return tokenList, adjustList
    if len(adjustList)==0:
        return tokenList, adjustList 

    def addRunning(running, Adj): 
        if Adj!=None: 
            running[0]=Adj[0]
            running[1]=Adj[1]
            running[2]=Adj[2]
            running[3]+=Adj[3]
        return running
    
    def addChange(running, tkn:FoundPotentialToken): #Might have issues at tkn lengths of 1
        if running[0]!=None and running[0]!=tkn.getSymbolIndex(): #No need to adjust length of string, just the index is required 
            tkn.setSymbolIndex(running[3]+tkn.getSymbolIndex()-1)
        else: 
            newStart=tkn.getStart()-running[2]-1 #old start - running end 
            newEnd=newStart+ tkn.getEnd()-tkn.getStart()
            newSymbolIdx=running[3] + tkn.getSymbolIndex() #running[3] counts how many words have been added total as a result of the breaks. For example Jacob...,,..., with ..., and ... takne results in 5 string, but only an increase of 4 in index. 
            tkn.setStart(newStart)
            tkn.setEnd(newEnd)
            tkn.setSymbolIndex(newSymbolIdx) 
 
    #assuming survivor fair list and problem lists are sorted by wordIndx, then by start
    running=[None, None, None, 0]
    adjIdx=0
    tknIdx=0 
    def assignNext():
        nonlocal adjIdx 
        adjIdx+=1
        if adjIdx>=len(adjustList):
            #adjIdx-=1 #extra detail for later
            return None
        else:
            return adjustList[adjIdx]
        
    nextAdj=adjustList[adjIdx] 

    skip=False 
    while adjIdx<len(adjustList) and tknIdx<len(tokenList):
        tkn=tokenList[tknIdx]
        print("1")  
        print("tkn: ",tkn,"\n", 
              "run: ",running,"\n",
              "nextAdj",nextAdj)
        


        if nextAdj[0]<tkn.getSymbolIndex():
            print("5")
            running=addRunning(running, nextAdj)  
            #Only adjust per difference in symbol Idx [until that Idx is handled?]
         
            nextAdj=assignNext()
            #maybe check on an assumption? 
        else: 
            if nextAdj[0]>tkn.getSymbolIndex():
                print("4") 
                if running[0]!=None: #Or adjIdx >0?
                    addChange(running, tkn)
                tknIdx+=1 
            else: #nextAdj[0]==tkn.getSymbolIdx()  
                if nextAdj[2]<tkn.getStart(): #Maybe we should compare start with start instead of end with start... just a thought.
                    print("3") 
                    running=addRunning(running, nextAdj)
                    nextAdj=assignNext()
                else:
                    print("2") 
                    if running[0]!=None: #Should also check running's [0]<=tkn symbol? maybe?
                        addChange(running, tkn)
                    tknIdx+=1 


    
    print("tkn: ",tkn,"\n", 
            "run: ",running,"\n",
            "nextAdj",nextAdj)
    if tknIdx<len(tokenList):
        print("7") 
        #First, make sure if nextAdj symbol is greater, that we catch up 
        #Then, allow the last thing to take place... 
        if nextAdj!=None: #Should always be unless a sudden break occurs above.
            while (nextAdj[0]>tkn.getSymbolIndex() and tknIdx<len(tokenList)):
                print("tkn: ",tkn,"\n", 
                    "run: ",running,"\n",
                    "nextAdj",nextAdj)
                tkn=tokenList[tknIdx] #tkn idx is gaurnteed not yet to have running applied to it from previous loop.
                if running[0] != None:
                    addChange(running, tkn)
                tknIdx+=1

            running=addRunning(running, nextAdj)
            nextAdj=None 

        while (tknIdx<len(tokenList)):
            tkn=tokenList[tknIdx]
            print("tkn: ",tkn,"\n", 
                "run: ",running,"\n",
                "nextAdj",nextAdj)
            if tkn.getSymbolIndex()==running[0]: #Propegate it out so what if we're bigger?
                print("8")
                if tkn.getStart()>running[2]:
                    addChange(running, tkn)
            elif tkn.getSymbolIndex()>running[0]:
                print("9")
                addChange(running, tkn)
            tknIdx+=1
 
    pass



#override 
def adjustTokens3(tokenList:list[FoundPotentialToken], adjustList:list[list[int,int,int,int]]):
     
    LastIdx=None
    ins=0
    for token in tokenList:
        for adjust in adjustList:
            if adjust[0]==token.getSymbolIndex():
                if adjust[2]<token.getStart(): 
                    ins+=1
            elif adjust[0]<token.getSymbolIndex():
                if LastIdx==None:
                    LastIdx=adjust[0]
                elif LastIdx==adjust[0]:
                    ins+=1
                else:
                    LastIdx=adjust[0] 

            #If adjust is > tokenSymbolIndex? We would add one to Ins and iterate Token I think


        print(token)          
        print("try an increase of ", ins) 
        
        ins=0
        LastIdx=None 
    ######
    ins=0
    LastIdx=None
    adjIdx=0
    tknIdx=0
    print("Trying together now")
    while adjIdx<len(adjustList) and tknIdx<len(tokenList):
        tkn=tokenList[tknIdx] 
        nextAdj=adjustList[adjIdx]
        if nextAdj[0]<tkn.getSymbolIndex():
            print("5") 
            adjIdx+=1  

            if LastIdx==None:
                LastIdx=nextAdj[0]
            elif LastIdx==nextAdj[0]:
                ins+=1
            else:
                LastIdx=nextAdj[0] 


        else: 
            if nextAdj[0]>tkn.getSymbolIndex():
                print("4")  
                tknIdx+=1 
                #ins+=1? #Don't increase insert amount, no split has occured.
                print("tkn: ",tkn, " try increase of ", ins) #Maybe LastIdx=None?
            else: #nextAdj[0]==tkn.getSymbolIdx()  
                if nextAdj[2]<tkn.getStart(): #Maybe we should compare start with start instead of end with start... just a thought.
                    print("3")  
                    adjIdx+=1
                    ins+=1 #Split occured
                else:
                    print("2")  
                    tknIdx+=1 
                    #ins+=1? #No split, so don't increase teh 'insert' amount, I think. Might have to check on a 1 lengt hhigh token...
                    print("tkn: ",tkn, " try increase of ", ins) #Maybe LastIdx=None?


    while tknIdx<len(tokenList):
        tkn=tokenList[tknIdx]
        print("tkn: ",tkn, " try increase of ", ins)
        tknIdx+=1
        #ins+=1 ? Only want to increase when a split occurs. Since no split occurs hence forth no need



 

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
    
    #NOTE
    #Need to test finding high tokens of length 1, 
        #Then accepting tokens of length 1 /create new line
            #then adjusting tokens of length 1... :/ 
    test=" "
    if test=="createNewLine2":
        inOrderSurvivor=[FoundPotentialToken("...", 0, 5, 7, 0)] 
        wordList=["Jacob...,,...",]
        line, adjusts=acceptToken(wordList, inOrderSurvivor) #Expect Jacob ... ,,...
        print("resulting line: ",line)
        print("adjustments : ", adjusts)
        print("BREAK 1")

        inOrder=[FoundPotentialToken("...", 0, 5, 7, 0),
                 FoundPotentialToken("...", 0, 10, 12, 0)]
        wordList=["Jacob...,,...",] 
        line, adjusts=acceptToken(wordList, inOrder) #expect jacob ... ,, ...
        print("resulting line: ",line)
        print("adjustments : ", adjusts)
        print("BREAK 2")
          

        inOrder=[FoundPotentialToken("...", 0, 5, 7, 0), FoundPotentialToken("...", 0, 5, 7, 1)]
        wordList=["Jacob...,,...,","Jacob...,,...,"] #expect Jacob ... ,,...,   x2
        line, adjusts=acceptToken(wordList, inOrder)
        print("resulting line: ",line)
        print("adjustments : ", adjusts)
        print("BREAK 3")

        inOrder=[FoundPotentialToken("...", 0, 5, 7, 0),
                 FoundPotentialToken("...", 0, 10, 12, 0),
                 FoundPotentialToken("...", 0, 5, 7, 1),
                 FoundPotentialToken("...", 0, 10, 12, 1)]
        line, adjusts=acceptToken(wordList, inOrder) #expect Jacob ... ,, ... , x2
        print("resulting line: ",line)
        print("adjustments : ", adjusts)
        print("BREAK 4")


        inOrder=[FoundPotentialToken("...", 0, 5, 7, 0),
                 FoundPotentialToken("...", 0, 10, 12, 0),
                 FoundPotentialToken("...", 0, 5, 7, 1) ] #Expect jacob ... ,, ... , jacob ... ,,...,
        line, adjusts=acceptToken(wordList, inOrder)
        print("resulting line: ",line)
        print("adjustments : ", adjusts)
        print("BREAK 5")

        #Then one at start, end, etc
        inOrder=[FoundPotentialToken("...", 0, 0, 2, 0),FoundPotentialToken("...", 0, 5, 7, 0), FoundPotentialToken("...", 0, 0, 2, 1), FoundPotentialToken("...", 0, 2, 4, 2)]
            #ERROR, problem when the index is at 0 for the hightoken... :/
        wordList=["...,,...", "...,,", ",,..."]
        line, adjusts=acceptToken(wordList, inOrder) #expect ... ,, ... ... ,, ,, ...
        print("resulting line: ",line)
        print("adjustments : ", adjusts)
        print("BREAK 6")




    test="adjustTokensLong"
    if test=="adjustTokensBasic":
    #survivorFairList:list[FoundPotentialToken], adjustList:list[list[int, int, int, int]]
        #TESTS BASED ON CREATENEWLINE returns
        inOrder=[FoundPotentialToken("...", 0, 5, 7, 0)] 
        wordList=["Jacob...,,...",]
        line, adjusts=acceptToken(wordList, inOrder) 
        print("resulting line: ",line)
        print("resulting adjusts: ", adjusts) 

        inOrderSurvivor=[FoundPotentialToken("...", 0, 10, 12, 0)]   
        adjustTokens3(inOrderSurvivor, adjusts)
        print(inOrderSurvivor) #Expect [2,4,2], 2 for token ,,... , 2,4 for start end.
        print("e [2,4,2]")
        print("\n")


        inOrder=[ 
                 FoundPotentialToken("...", 0, 10, 12, 0)]
        wordList=["Jacob...,,...",] 
        line, adjusts=acceptToken(wordList, inOrder) #expect jacob ... ,, ...
        print("resulting line: ",line) 
        print("resulting adjusts: ", adjusts) 
        inOrderSurvivor=[FoundPotentialToken("...", 0, 5, 7, 0)]   
        adjustTokens3(inOrderSurvivor, adjusts)
        print(inOrderSurvivor) #Expect [5,7,0], as the change shouldn't affect it since it starts before and cahgnes are made
        print("e [5,7,0]")
        print("\n")
        

    #ISSUE lingering six at end!
        inOrder=[FoundPotentialToken("...", 0, 5, 7, 0), FoundPotentialToken("...", 0, 5, 7, 1)]
        wordList=["Jacob...,,...,","Jacob...,,...,"] #expect Jacob ... ,,...,   x2
        line, adjusts=acceptToken(wordList, inOrder)
        print("resulting line: ",line)
        print("resulting adjusts: ", adjusts) 
        inOrderSurvivor=[FoundPotentialToken("...", 0, 10, 12, 0),FoundPotentialToken("...", 0, 10, 12, 1)]  
        adjustTokens3(inOrderSurvivor, adjusts)
        print(inOrderSurvivor)    #expect [2, 4, 2], [2,4,5]
        print("e [2, 4, 2], [2,4,5]")
        print("\n")
        #We end up in a situation which asks us to choose between 1+3=4, or 1+5=6, so no wonder I'm having such toruble with the algorithm. There must be some other conditional I'm missing... Or this is a fools errand.
        

    #ISSUE Lingering six at start
        inOrder=[FoundPotentialToken("...", 0, 5, 7, 0),
                 FoundPotentialToken("...", 0, 10, 12, 0)]
        line, adjusts=acceptToken(wordList, inOrder) #expect Jacob ... ,, ... , x2
        print("resulting line: ",line)   
        print("resulting adjusts: ", adjusts) 
        inOrderSurvivor=[FoundPotentialToken("...", 0, 5, 7, 1),
                 FoundPotentialToken("...", 0, 10, 12, 1)]   
        adjustTokens3(inOrderSurvivor, adjusts)
        print(inOrderSurvivor)    #expect [5, 7, 5], [10, 12, 5]
        print("e [5, 7, 5], [10, 12, 5]")
        print("\n")
        

        inOrder=[FoundPotentialToken("...", 0, 5, 7, 1),
                 FoundPotentialToken("...", 0, 10, 12, 1) ]
        line, adjusts=acceptToken(wordList, inOrder) #expect Jacob ... ,, ... , x2
        print("resulting line: ",line)   
        inOrderSurvivor=[FoundPotentialToken("...", 0, 5, 7, 0),
                 FoundPotentialToken("...", 0, 10, 12, 0)]   
        adjustTokens3(inOrderSurvivor, adjusts)
        print(inOrderSurvivor)    #expect [5, 7, 0], [10, 12, 0]
        print("e [5, 7, 0], [10, 12, 0]")
        print("\n")

        if (False):
            #Later
            inOrder=[FoundPotentialToken("...", 0, 5, 7, 0),
                    FoundPotentialToken("...", 0, 10, 12, 0),
                    FoundPotentialToken("...", 0, 5, 7, 1) ] #Expect jacob ... ,, ... , jacob ... ,,...,
            line, adjusts=acceptToken(wordList, inOrder)
            #print("resulting line: ",line)  
            #Then one at start, end, etc
            inOrder=[FoundPotentialToken("...", 0, 0, 2, 0),FoundPotentialToken("...", 0, 5, 7, 0), FoundPotentialToken("...", 0, 0, 2, 1), FoundPotentialToken("...", 0, 2, 4, 2)]
                #ERROR, problem when the index is at 0 for the hightoken... :/
            wordList=["...,,...", "...,,", ",,..."]
            line, adjusts=acceptToken(wordList, inOrder) #expect ... ,, ... ... ,, ,, ...
            #print("resulting line: ",line) 

    if test=="adjustTokensLong":
        #jacob-...-,,..., NOBREAK jacob...,,...,
        inOrder=[FoundPotentialToken("...", 0, 5, 7, 0), 
                ] 
        wordList=["Jacob...,,...,","NOBREAK", "Jacob...,,...,"]
        line, adjusts=acceptToken(wordList, inOrder) 
        print("resulting line: ",line)
        print("resulting adjusts: ", adjusts) 

        inOrderSurvivor=[FoundPotentialToken("...", 0, 10, 12, 0), FoundPotentialToken("...", 0, 5, 7, 2),FoundPotentialToken("...", 0, 10, 12, 2)]   
        adjustTokens3(inOrderSurvivor, adjusts)
        print(inOrderSurvivor) 
        print("e [2,4,2], [5,7,4], [10,12,4]")
        print("\n")

        #jacob...-,,-...-, NOBREAK jacob-...-,,...,
        inOrder=[FoundPotentialToken("...", 0, 5, 7, 0),
                FoundPotentialToken("...", 0, 10, 12, 0),
                FoundPotentialToken("...", 0, 5, 7, 2)
                ] 
        wordList=["Jacob...,,...,","NOBREAK", "Jacob...,,...,"]
        line, adjusts=acceptToken(wordList, inOrder) 
        print("resulting line: ",line)
        print("resulting adjusts: ", adjusts) 

        inOrderSurvivor=[FoundPotentialToken("...", 0, 10, 12, 2)]   
        adjustTokens3(inOrderSurvivor, adjusts)
        print(inOrderSurvivor) 
        print("e [2,4,8]")
        print("\n")


        #jacob...-,,-...-, NOBREAK jacob-...-,,...,
        inOrder=[FoundPotentialToken("...", 0, 5, 7, 0),
                FoundPotentialToken("...", 0, 10, 12, 0), 
                FoundPotentialToken("...", 0, 5, 7, 1),
                FoundPotentialToken("...", 0, 5, 7, 2)
                ] 
        wordList=["Jacob...,,...,","Jacob...,,...,", "Jacob...,,...,"]
        line, adjusts=acceptToken(wordList, inOrder) 
        print("resulting line: ",line)
        print("resulting adjusts: ", adjusts) 

        inOrderSurvivor=[FoundPotentialToken("...", 0, 10, 12, 1), FoundPotentialToken("...", 0, 10, 12, 2)]   
        adjustTokens3(inOrderSurvivor, adjusts)
        print(inOrderSurvivor) 
        print("e [2,4,7], [2,4,10]")
        print("\n")
        



    #When adjusting, if we had more than 1 split... I wonder about it... I think it's fine... [symbol index, start end of word, and indexes t oadjust by [add to it]]
    



if __name__=="__main__":
    main()